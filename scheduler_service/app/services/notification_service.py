import requests

NOTIFY_URL = "http://imap_service:8000/notify"

def sendNotification(to, subject, message):
    try:
        payload = {"to": to, "subject": subject, "message": message}
        response = requests.post(NOTIFY_URL, json=payload, timeout=3)
        response.raise_for_status()
    except Exception as e:
        print(f"[NOTIFICATION ERROR] {e}")
