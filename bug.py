import time # or DATETIME?
import threading

import web
import model

from twilio.rest import TwilioRestClient



twilio_number = "+16507275900" # HIDE this somewhere?

urls = (
    '/', 'receive_message',
)


# Used to see if anything needs to be sent
SWEEP_FREQUENCY = 60 #seconds
def sweep():
    threading.Timer(SWEEP_FREQUENCY, sweep).start()
    for reminder in reminder_db:
        if reminder.send_at < time.time(): #or whatever
            send_message(reminder)
            reminder.send_at += reminder.interval
# Starts the loop
sweep()



def send_message(message, recipient):
  twilio.send(message, recipient) ... whatever

################# All from the twilio website, verbatim:
# https://www.twilio.com/docs/api/rest/sending-messages#post
#################
    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = "AC8554a81ca9d1b4658093bfc4a0dc23d1"
    auth_token  = "{{ auth_token }}"
    client = TwilioRestClient(account_sid, auth_token)

    # 0aea2768b7cb3dfe1d74c6a03e8a9dc7 ... ?

    message = client.messages.create(
        body=message,
        to="+1"+recipient,
        from_=twilio_number )
    print message.sid
################





class receive_message(message):
    text, number = parse_message(message)
    if len(pieces) > 1:
        activate_reminder(*pieces)
    elif len(pieces)==1:# and pieces[0].split(" ")[0].lower()=='did':

        inactivate_reminder(name)

    else:
        # it wasn't properly formatted
        couldnt_parse(number)


app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
