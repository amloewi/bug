import time # or DATETIME?
import threading
import cgi

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


#wsgi.input: <webd.wsgiserver.KnonwnLengthRFile object>

class receive_message:

    def GET(self):
        return render.home()

    def POST(self):
        # WHY IS THIS SO NUTS?
        # This will all get folded into parse_message
        request = cgi.FieldStorage()
        print request['Body']
        print request['FromCity']

        # raw_request = web.ctx.env['wsgi.input'].read()
        # request
        # text = cgi.FieldStorage.getvalue(request, 'Body')
        # number =
        # print cgi.FieldStorage.getvalue("""ToCountry=US&ToState=CA&SmsMessageSid=SMf3893b4c2ccf025cd4b6efe741431e8d
        # &NumMedia=0&ToCity=&FromZip=94304&SmsSid=SMf3893b4c2ccf025cd4b6efe741431e8d
        # &FromState=CA&SmsStatus=received&FromCity=PALO+ALTO&Body=Hello+bug&FromCountry=US
        # &To=%2B16507275900&ToZip=&MessageSid=SMf3893b4c2ccf025cd4b6efe741431e8d
        # &AccountSid=AC8554a81ca9d1b4658093bfc4a0dc23d1
        # &From=%2B16503915900&ApiVersion=2010-04-01"""
        # , 'Body')
        #length = int(self.headers["Content-Length"])
        #print("Data: " + str(self.rfile.read(length), "utf-8"))

        #print "message: ", web.ctx.query

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
