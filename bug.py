import time # or DATETIME?
import threading

import web
import model

from twilio.rest import TwilioRestClient



twilio_number = "+16507275900" # HIDE this somewhere?

urls = (
    # The twilio request URL needs to be set to the homepage
    '/', 'receive_message',
)

render = web.template.render('templates')



# # Used to see if anything needs to be sent
# SWEEP_FREQUENCY = 60 #seconds
# def sweep():
#     threading.Timer(SWEEP_FREQUENCY, sweep).start()
#     for reminder in reminder_db:
#         if reminder.send_at < time.time(): #or whatever
#             send_message(reminder)
#             reminder.send_at += reminder.interval
# # Starts the loop
# sweep()


def send_message(message, number):

    account_sid = "AC8554a81ca9d1b4658093bfc4a0dc23d1"
    auth_token  = "{{ auth_token }}"
    client = TwilioRestClient(account_sid, auth_token)

    # 0aea2768b7cb3dfe1d74c6a03e8a9dc7 ... ?

    message = client.messages.create(
        body=message,
        to="+1"+number,
        from_=twilio_number )

def parse_message(message):
    pass

def new_reminder():
    pass

def inactivate_reminder():
    pass

def couldnt_parse():
    pass




class receive_message:

    def GET(args):
        return render.home()

    def POST(args):
        print "message: ", message

        # text, number, kind = parse_message(message)
        # if kind=="new":
        #     new_reminder(text)
        # elif kind=="inactivate":
        #     inactivate_reminder(text)
        # else: # kind=="wrong"
        #     # it wasn't properly formatted
        #     couldnt_parse(number)


app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
