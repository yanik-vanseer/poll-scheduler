from app.rest_client import createPoll, voteOnPoll

def processIncomingEmail(subject, sender, body):
    subjectLower = subject.lower()

    if "create poll" in subjectLower:
        emails = extractListFromLine(body, "emails:")
        dates = extractListFromLine(body, "dates:")
        location = extractListFromLine(body, "location")
        if not emails or not dates:
            return
        createPoll(sender, emails, dates, location)

    elif "vote on poll" in subjectLower:
        pollId = extractValueFromLine(body, "poll_id:")
        dates = extractListFromLine(body, "dates:")
        if not pollId or not dates:
            return
        voteOnPoll(pollId, sender, dates)

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