from app.rest_client import createPoll, voteOnPoll
from app.notification_server import sendEmail

from app.rest_client import createPoll, voteOnPoll
from app.notification_server import sendEmail

def processIncomingEmail(subject, sender, body):
    subjectLower = subject.lower()

    try:
        if "create poll" in subjectLower:
            emails = extractListFromLine(body, "emails:")
            dates = extractListFromLine(body, "dates:")
            location = extractListFromLine(body, "location")

            if not emails or not dates or not location:
                raise Exception("Missing required fields for poll creation")

            createPoll(sender, emails, dates, location)

        elif "vote on poll" in subjectLower:
            pollId = extractValueFromLine(body, "poll_id:")
            dates = extractListFromLine(body, "dates:")

            if not pollId or not dates:
                raise Exception("Missing required fields for voting")

            voteOnPoll(pollId, sender, dates)

        else:
            raise Exception("Unrecognized subject")

    except Exception:
        sendEmail(
            to=sender,
            subject="We could not process your email",
            body=(
                "We couldn't process your email request.\n\n"
                "Please use one of the following two formats:\n\n"
                "1. Subject: create poll\n"
                "Body:\n"
                "emails: alice@example.com, bob@example.com\n"
                "dates: 15-05-2025, 16-05-2025\n"
                "location: Brussels\n\n"
                "2. Subject: vote on poll\n"
                "Body:\n"
                "poll_id: <your-poll-id>\n"
                "dates: 15-05-2025, 16-05-2025\n\n"
                "Make sure all required fields are present and formatted correctly."
            )
        )

def extractListFromLine(text, prefix):
    for line in text.splitlines():
        if line.lower().startswith(prefix.lower()):
            items = line.split(":", 1)[1]
            return [item.strip() for item in items.split(",")]
    return []

def extractValueFromLine(text, prefix):
    for line in text.splitlines():
        if line.lower().startswith(prefix.lower()):
            return line.split(":", 1)[1].strip()
    return None