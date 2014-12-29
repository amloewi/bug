import web
import twilio
import time

urls = (
    '/', 'home',
)

def nothin():
    return 4

def receive_message(message):
  pieces = parse_into_reminder(message)
  return insert_into_reminder_db(*pieces)

def send_message(message, recipient):
  twilio.send(message, recipient) ... whatever


class Reminder:
    def __init__(self, name, message, interval):
        # The identifier. Used to shut a reminder off. "Did name"
        self.name = name
        # The reminder itself. Appears as "Name: message" in the SMS
        self.message = message
        # Entered in minutes, but time.time is in seconds.
        self.interval = interval*60
        self.send_at = time.time() + interval*60
        # A feature for ... NUMBER of repeats?

    def

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()


  # on a loop ... every 60? seconds, check.
  for reminder in reminder_db:
    if reminder.send_at < time.time(): #or whatever
      send_message(reminder)
      reminder.send_at += reminder.interval
