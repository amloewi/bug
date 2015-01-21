import time
import os
import copy
# Thought time was a problem, and thought only loading functions might be faster
from threading import Timer
from cgi import parse_qs
from urllib2 import urlopen

import web
import model

from twilio.rest import TwilioRestClient


#################
##### URLS ######
#################

urls = (
    # The twilio request URL needs to be set to the homepage
    '/', 'receive_message',
)


####################
##### GLOBALS ######
####################

# The twilio number that receives (and sends) the texts
twilio_number = os.environ['TWILIO_NUMBER']#"+16507275900" # HIDE this somewhere?
# Default number of minutes in between reminders
INTERVAL_DEFAULT = 30
# Default number of times a message is repeated before inactivation
REPEATS_DEFAULT = 5
# The interval at which the database is checked for queued messages
if os.path.abspath("") == '/Users/alexloewi/Documents/Sites/bug':
  SWEEP_FREQUENCY = 10 # second -- debugging mode.
else:
  SWEEP_FREQUENCY = 5*60 #seconds, i.e. 5 minutes, normally.



#####################################
##### NECESSARY FRAMEWORK CALLS #####
#####################################

app = web.application(urls, globals())
render = web.template.render('templates')


######################
##### FUNCTIONS ######
######################

def send_message(to, message):

    account_sid = "AC8554a81ca9d1b4658093bfc4a0dc23d1"
    auth_token  = os.environ['TWILIO_AUTH_TOKEN'] #"0aea2768b7cb3dfe1d74c6a03e8a9dc7" #"{{ auth_token }}"
    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(
        body=message,
        to=to,
        from_=twilio_number)


# Used to see if anything needs to be sent
def sweep():
    Timer(SWEEP_FREQUENCY, sweep).start()
    now = time.time()
    reminders = model.get_active()
    if reminders:
        # This will just ping the site IFF there are active reminders.
        # Keeps it awake for > 1hr.
        # This has caused trouble before, but I don't know why.
        #urlopen('http://sikeda.herokuapp.com')
        pass
    for reminder in reminders:
        if now > reminder.send_at:
            send_message(reminder.sender_number, reminder.message)
            # GOTTA PUT THIS BACK IN THE DB
            reminder.send_at += reminder.interval
            reminder.times_sent += 1
            if reminder.repeats_left > 0:
                reminder.repeats_left -= 1
                model.reinsert(reminder)
            else:
              model.inactivate_reminder(reminder.sender_number,
                                        reminder.name.strip(),
                                        "ran_out")
              msg = "Your reminder \'"+reminder.name.strip()+"\' just ran out."
              send_message(reminder.sender_number, msg)

############################
###### Starts the loop #####
############################
# This is done here just so as to be close to the function itself, which is
# not exactly a function like the others
sweep()


# def couldnt_parse():
#     pass


def parse_message(test_request=None):
  """Parses the web request from a twilio message, returns request and message

  In other words, there's lots that comes from the web: routing address,
  wsgi stuff, etc. This picks out the actual text message content, because
  that's what has the 'bug' arguments. Also returns how many of these there are,
  because that gets used a lot of times. Splits the message into arguments,
  casts the numbers as integers when they're there, and finally sticks the
  sender's number on the FRONT of the list, so that default interval and repeat
  args can be easily appended to the END without messing up the order.

  """

  if test_request:
    request = test_request
  else:
    raw_string = web.ctx.env['wsgi.input'].read()
    # Function's a little weird. Instead of returning str:str, it gives
    # str:[str], i.e. 'Body': ['Hello Bug']
    request = parse_qs(raw_string)

  text = request['Body'][0]
  sender = request['From'][0]

  # Cuts it into "m-s-g" "number?" "number?""
  msg_args = [piece.strip() for piece in text.split()]

  flag = msg_args[0].lower()
  # Allows for messages that start with Did or Cancel,
  # AS LONG AS they have MORE than two words.
  if flag == "did" or flag == "cancel" and len(msg_args)==2:

    # Remove a period(/space), i.e. "ant. " => "ant"
    msg_args[-1] = msg_args[-1].replace(".","").strip()

    msg_args.insert(0, sender)

    # [sender, did/cancel, job]
    return msg_args, flag

  else:

    numbers = []
    for i in range(2):
      if msg_args[-1].isdigit():
        numbers.append(int(msg_args.pop()))

    numbers.reverse()
    # [re-joined-message, param?, param?]
    msg_args = [" ".join(msg_args)] + numbers

    msg_args.insert(0, sender)

    # [sender, msg, (, param (, param))]
    return msg_args, "new_message"



def add_defaults(args):
  """ Adds the default arguments for the interval and repeats, if necessary.

  """

  msg_args = copy.copy(args)

  # sender, message
  if len(msg_args) == 2:
    msg_args += [INTERVAL_DEFAULT, REPEATS_DEFAULT]
  # sender, message, interval
  elif len(msg_args) == 3:
    msg_args += [REPEATS_DEFAULT]
  else:
    pass # it had everything

  return msg_args



####################################
##### THE WEB PAGES THEMSELVES #####
####################################

class receive_message:

    def GET(self):
        return render.home()

    def POST(self):

        msg_args, msg_type = parse_message()

        # Handles both "completed" and "cancel"?
        if msg_type=="did" or msg_type=="cancel":

          sender, message, job = msg_args

          to, job = model.inactivate_reminder(sender, job, msg_type)

          msg = "Your reminder \'"+job+"\' was stopped."

          send_message(to, msg)

        elif msg_type=="new_message":

          msg_args = add_defaults(msg_args)

          to, job = model.new_reminder(*msg_args)

          msg = "Your reminder was given the name \'"+job+"\'."

          send_message(to, msg)

        else:
          # Incorrect formatting or something -- tell sender?
          pass


if __name__ == "__main__":
    app.run()

    # m = {'From': ["+16503915900"], 'Body':["Blah blah blah 1 2"] }
    # msg_args, msg_type = parse_message(m)
    # #print "both", msg_args, msg_type
    # if msg_type == "new_message":
    #   msg_args = add_defaults(msg_args)
    #   #print "msg_args: ", msg_args
    #   model.new_reminder(*msg_args)
    #
    # m = {'From': ["+16503915900"], 'Body':["did beetle."] }
    # msg_args, msg_type = parse_message(m)
    #
    # #print "msg_args pre inactivate: ", msg_args
    # model.inactivate_reminder(msg_args[0], msg_args[2], msg_type)


  # This is just an example, for reference, of the format of web request.
    # print cgi.parse_qs("""ToCountry=US&ToState=CA&SmsMessageSid=SMf3893b4c2ccf025cd4b6efe741431e8d
    # &NumMedia=0&ToCity=&FromZip=94304&SmsSid=SMf3893b4c2ccf025cd4b6efe741431e8d
    # &FromState=CA&SmsStatus=received&FromCity=PALO+ALTO&Body=Hello+bug&FromCountry=US
    # &To=%2B16507275900&ToZip=&MessageSid=SMf3893b4c2ccf025cd4b6efe741431e8d
    # &AccountSid=AC8554a81ca9d1b4658093bfc4a0dc23d1
    # &From=%2B16503915900&ApiVersion=2010-04-01"""
    # )
