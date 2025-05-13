# Business logic for the flask application

import json
from collections import Counter
from app.db.database import db
from app.models.poll_model import Poll
from app.models.vote_model import Vote
from app.services.notification_service import sendNotification
from app.services.weather_service import getWeatherForecast

# Adds a poll to the database
def addPoll(sender, emails, dates, location):
    if not sender or not emails or not dates:
        raise ValueError("Sender, emails and dates are required.")

    emails_json = json.dumps(emails)
    dates_json = json.dumps(dates)

    new_poll = Poll(
        organiser=sender,
        invited_emails=emails_json,
        available_dates=dates_json
    )

    db.session.add(new_poll)
    db.session.commit()

    poll_id = new_poll.id

    weather_info = getWeatherForecast(dates, location)

    # Notification based on the circumstance
    for email in emails:
        sendNotification(
            to=email,
            subject="You're invited to vote in a poll",
            message=(
                f"You have been invited to vote in a date poll created by {sender}.\n\n"
                f"Poll ID: {poll_id}\n\n"
                f"Available dates and weather forecast:\n" +
                "\n".join(f"- {date}: {weather_info.get(date, 'Unknown')}" for date in dates) +
                "\n\nTo vote, reply to this email with:\n"
                f"For instance, if you are available at all dates:\n"
                f"Subject: vote on poll\n\n"
                f"And in the body:\n"
                f"poll_id: {poll_id}\n"
                f"dates: {', '.join(dates)}\n\n"
                "Thank you for your participation."
            )
        )


    sendNotification(
        to=sender,
        subject="Your poll has been created",
        message=(
            f"Your poll has been successfully created with ID: {poll_id}\n\n"
            f"Participants can use this poll ID to cast their votes.\n"
            f"Invitations have been sent to {len(emails)} recipients."
        )
    )
    
    return poll_id

# Adds a vote to the database for a specific poll
def addVote(poll_id, sender, dates):
    if not poll_id or not sender or not dates:
        raise ValueError("Poll ID, sender and dates are required.")
    
    poll = Poll.query.get(poll_id)
    if not poll:
        raise ValueError(f"Poll with ID {poll_id} does not exist.")

    dates_json = json.dumps(dates)

    existing_vote = Vote.query.filter_by(poll_id=poll_id, voter_email=sender).first()

    # Updates existing vote or else creates a new one for the poll
    if existing_vote:
        existing_vote.selected_dates = dates_json
        existing_vote.created_at = db.func.now()
        db.session.commit()
        vote_id = existing_vote.id
    else:
        new_vote = Vote(
            poll_id=poll_id,
            voter_email=sender,
            selected_dates=dates_json
        )

        db.session.add(new_vote)
        db.session.commit()
        vote_id = new_vote.id

    # Try to finallize the poll
    final_date = tryFinalizePoll(poll)

    all_recipients = json.loads(poll.invited_emails)
    all_recipients.append(poll.organiser)
    all_recipients = list(set(all_recipients))

    # Notification based on the circumstance
    if final_date:
        for email in all_recipients:
            sendNotification(
                to=email,
                subject="Poll finalized",
                message=(
                    f"The poll with ID {poll.id} has been finalized.\n"
                    f"The selected date is: {final_date}"
                )
            )
    else:
        for email in all_recipients:
            if email != sender:
                sendNotification(
                    to=email,
                    subject="New vote received",
                    message=(
                        f"{sender} has just submitted a vote in poll ID {poll.id}."
                    )
                )

    return vote_id

# Attempts to finalize the poll by selecting the most common voted date if all have voted
def tryFinalizePoll(poll: Poll):
    invited = set(json.loads(poll.invited_emails))
    votes = Vote.query.filter_by(poll_id=poll.id).all()
    voters = set(v.voter_email for v in votes)

    if not invited.issubset(voters):
        return None

    all_dates = []
    for v in votes:
        all_dates.extend(json.loads(v.selected_dates))
    
    final_date, _ = Counter(all_dates).most_common(1)[0]
    poll.confirmed_date = final_date
    db.session.commit()
    return final_date