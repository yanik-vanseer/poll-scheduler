import threading
from app.notification_server import app as flaskApp
from app.email_monitor import monitorInbox

def runFlask():
    flaskApp.run(host="0.0.0.0", port=8000)

def runImapMonitor():
    monitorInbox()

if __name__ == "__main__":
    t1 = threading.Thread(target=runFlask)
    t2 = threading.Thread(target=runImapMonitor)

    t1.start()
    t2.start()

    t1.join()
    t2.join()