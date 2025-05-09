from imapclient import IMAPClient
import pyzmail
import os, time
from dotenv import load_dotenv
from app.email_parser import processIncomingEmail

load_dotenv("/app/.env")
EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = "imap.gmail.com"
CHECK_INTERVAL = 30

def monitorInbox():
    imap = None
    try:
        imap = IMAPClient(IMAP_SERVER, ssl=True)
        imap.login(EMAIL, PASSWORD)
        imap.select_folder('INBOX', readonly=True)

        # Fetches amount of emails in the inbox
        knownUids = set(imap.search(['ALL']))

        # Main loop for monitoring the inbox
        while True:
            time.sleep(CHECK_INTERVAL)
            try:
                imap.select_folder('INBOX', readonly=True)
                currentUids = set(imap.search(['ALL']))

                # Compares old to new amount of emails
                newUids = currentUids - knownUids

                # if newUids is above zero (when there are new emails) the incoming emails get processed
                if newUids:
                    for uid in sorted(newUids):
                        rawMessage = imap.fetch([uid], ['BODY[]'])
                        message = pyzmail.PyzMessage.factory(rawMessage[uid][b'BODY[]'])

                        subject = message.get_subject()
                        sender = message.get_addresses('from')[0][1]
                        body = message.text_part.get_payload().decode(message.text_part.charset)
                        
                        processIncomingEmail(subject, sender, body)

                    knownUids.update(newUids)
            except Exception as e:
                print(f"[ERR] Error during check loop {e}")
                time.sleep(5)

    except Exception as conn_err:
        print(f"[ERR] Error during connection {conn_err}")
    finally:
        # Always attempt to cleanly close the IMAP connection, even in case of errors
        if imap:
            try:
                imap.logout()
            except Exception as logout_err:
                print(f"[ERR][ERROR during logout] {logout_err}")