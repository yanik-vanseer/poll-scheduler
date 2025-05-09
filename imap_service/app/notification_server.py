# Separate Flask application for handling notifications sent by the scheduler_service

from flask import Flask, request, jsonify
from email.mime.text import MIMEText
import smtplib
import os
from dotenv import load_dotenv

load_dotenv("/app/.env")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

app = Flask(__name__)

# Sends an email from the configured address to the specified recipient
def sendEmail(to, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, [to], msg.as_string())

    except Exception as e:
        print(f"[ERR] Failed to send email to {to}: {e}")
        raise e

# Endpoint to receive and process notification requests from the scheduler_service
@app.route("/notify", methods=["POST"])
def notify():
    data = request.get_json()

    if not data or not all(k in data for k in ("to", "subject", "message")):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    try:
        sendEmail(data["to"], data["subject"], data["message"])
        return jsonify({"status": "sent"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500