# Connection to the scheduler_service microservice

import requests

POLL_SERVICE_BASE = "http://scheduler_service:5000/polls"

def createPoll(sender, emails, dates, location):
    payload = {
        "sender": sender,
        "emails": emails,
        "dates": dates,
        "location": location
    }
    try:
        requests.post(f"{POLL_SERVICE_BASE}/create", json=payload, timeout=5)
    except requests.RequestException as e:
        print(f"[ERR] Failed to create poll: {e}")

def voteOnPoll(pollId, sender, selectedDates):
    payload = {
        "poll_id": pollId,
        "sender": sender,
        "selected_dates": selectedDates
    }
    try:
        requests.post(f"{POLL_SERVICE_BASE}/vote", json=payload, timeout=5)
    except requests.RequestException as e:
        print(f"[ERR] Failed to submit vote: {e}")