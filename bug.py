import time
import threading import Timer
from cgi import parse_qs
from urllib2 import urlopen

import web
import model

from twilio.rest import TwilioRestClient



twilio_number = "+16507275900" # HIDE this somewhere?
my_number = "+16503915900"

urls = (
    # The twilio request URL needs to be set to the homepage
    '/', 'receive_message',
)

app = web.application(urls, globals())

render = web.template.render('templates')



def send_message(reminder):

    account_sid = "AC8554a81ca9d1b4658093bfc4a0dc23d1"
    auth_token  = "0aea2768b7cb3dfe1d74c6a03e8a9dc7" #"{{ auth_token }}"
    client = TwilioRestClient(account_sid, auth_token)

    # 0aea2768b7cb3dfe1d74c6a03e8a9dc7 ... ?

    message = client.messages.create(
        body=reminder.name.strip() + ": "+ reminder.message.strip(),
        to=reminder.sender_number,
        from_=twilio_number)


# Used to see if anything needs to be sent
SWEEP_FREQUENCY = 5*60 #seconds
def sweep():
    Timer(SWEEP_FREQUENCY, sweep).start()
    now = time.time()
    reminders = model.get_active()
    if reminders:
        # This will just ping the site IFF there are active reminders. Keeps it awake for > 1hr.
        urlopen('http://sikeda.herokuapp.com')
    for reminder in reminders:
        if now > reminder.send_at:
            send_message(reminder)
            # GOTTA PUT THIS BACK IN THE DB
            reminder.send_at += reminder.interval
            reminder.times_sent += 1
            if reminder.repeats_left > 0:
                reminder.repeats_left -= 1
            model.reinsert(reminder)

# Starts the loop
sweep()



# def parse_message(message):
#     pass
#
# def new_reminder(name, msg, interval, repeats):
#     pass
#
# def inactivate_reminder(name):
#     pass
#
# def couldnt_parse():
#     pass



class receive_message:

    def GET(self):
        return render.home()

    def POST(self):
        # WHY IS THIS SO NUTS?
        # This will all get folded into parse_message
        raw_string = web.ctx.env['wsgi.input'].read()
        # Function's a little weird. Instead of returning str:str, it gives
        # str:[str], i.e. 'Body': ['Hello Bug']
        request = parse_qs(raw_string)
        text = request['Body'][0]

        msg_args = text.split(",")
        num_args = len(msg_args)
        if num_args==1:
            #kind = "inactivate"
            did, name = msg_args[0].split(" ")[0:2] # Ignores anything after.

            if did.lower() == "did":
                model.inactivate_reminder(name)
            else:
                # improperly formatted -- say so.
                pass

        # name, msg, interval (, repeats)
        elif num_args==3 or num_args==4:
            pieces = text.split(",")
            pieces = [p.strip() for p in pieces]
            pieces[2] = int(pieces[2]) #it's all strings right now
            if num_args==3:
                # The default 'number of repeats' argument.
                pieces.append(5)
            else:
                # Gotta cast the repeat argument, IF it's there.
                pieces[-1] = int(pieces[-1])
            pieces.append(request['From'][0])
            model.new_reminder(*pieces)

        else:
            # Incorrect number of arguments -- tell sender.
            pass



        # print cgi.parse_qs("""ToCountry=US&ToState=CA&SmsMessageSid=SMf3893b4c2ccf025cd4b6efe741431e8d
        # &NumMedia=0&ToCity=&FromZip=94304&SmsSid=SMf3893b4c2ccf025cd4b6efe741431e8d
        # &FromState=CA&SmsStatus=received&FromCity=PALO+ALTO&Body=Hello+bug&FromCountry=US
        # &To=%2B16507275900&ToZip=&MessageSid=SMf3893b4c2ccf025cd4b6efe741431e8d
        # &AccountSid=AC8554a81ca9d1b4658093bfc4a0dc23d1
        # &From=%2B16503915900&ApiVersion=2010-04-01"""
        # )

        # text, number, kind = parse_message(message)
        # if kind=="new":
        #     new_reminder(text)
        # elif kind=="inactivate":
        #     inactivate_reminder(text)
        # else: # kind=="wrong"
        #     # it wasn't properly formatted
        #     couldnt_parse(number)


if __name__ == "__main__":
    app.run()
