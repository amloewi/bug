import time
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
twilio_number = "+16507275900" # HIDE this somewhere?
# Default number of minutes in between reminders
INTERVAL_DEFAULT = 30
# Default number of times a message is repeated before inactivation
REPEATS_DEFAULT = 5
# The interval at which the database is checked for queued messages
SWEEP_FREQUENCY = 5*60 #seconds, i.e. 5 minutes



#####################################
##### NECESSARY FRAMEWORK CALLS #####
#####################################

app = web.application(urls, globals())
render = web.template.render('templates')


######################
##### FUNCTIONS ######
######################

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
def sweep():
    Timer(SWEEP_FREQUENCY, sweep).start()
    now = time.time()
    reminders = model.get_active()
    if reminders:
        # This will just ping the site IFF there are active reminders.
        # Keeps it awake for > 1hr.
        # This has caused trouble before, but I don't know why.
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
            else:
              pass
              #model.inactivate_reminder(reminder.name)

############################
###### Starts the loop #####
############################
# This is done here just so as to be close to the function itself, which is
# not exactly a function like the others
sweep()


# def couldnt_parse():
#     pass


def parse_message():
  """Parses the web request from a twilio message, returns request and message

  In other words, there a ton of stuff that comes from the web: routing address,
  wsgi stuff, etc. This picks out the actual text message content, because
  that's what has the 'bug' arguments. Also returns how many of these there are,
  because that gets used a lot of times. Splits the message into arguments,
  casts the numbers as integers when they're there, and finally sticks the
  sender's number on the FRONT of the list, so that default interval and repeat
  args can be easily appended to the END without messing up the order.

  """

  # WHY IS THIS SO NUTS?
  # This will all get folded into parse_message
  raw_string = web.ctx.env['wsgi.input'].read()
  # Function's a little weird. Instead of returning str:str, it gives
  # str:[str], i.e. 'Body': ['Hello Bug']
  request = parse_qs(raw_string)

  text = request['Body'][0]
  msg_args = [piece.strip() for piece in text.split(",")]
  # Cast the interval and repeats as numbers, IF they're there.
  msg_args = [int(arg) if i >= 2 else arg for i, arg in enumerate(msg_args)]
  num_args = len(msg_args)

  sender = request['From'][0]
  # Insert works as 'INDEX, argument' which I always find weird.
  msg_args.insert(0, sender)

  return msg_args, num_args


def inactivate_reminder(args):
  """Responds to a message of the format "Did <job name>," stops reminder 'job'

  Simple. Parses, checks to make sure the command looks like it should,
  and passes the name of the requested job off to the database. It's THERE
  that things are dealt with if such a job cannot be found.
  """

  # Indexing: skip 'sender' in args at 0, ignore after 'did <name>' in message
  did, name = [p.strip() for p in args[1].split(" ")[0:2]]

  # Just making sure.
  if did.lower() == "did":
      response = model.inactivate_reminder(name)
      # if response says 'no such job', tell the user.
  else:
      # improperly formatted -- say so.
      pass


def add_defaults(args, num_args):
  """ Adds the default arguments for the interval and repeats, if necessary.


  """

  msg_args = copy.copy(args)
  # If it doesn't have an interval,
  if num_args < 4:
    msg_args.append(INTERVAL_DEFAULT)
    # If it doesn't have repeats,
    if num_args < 4:
      msg_args.append(REPEATS_DEFAULT)

  return msg_args



####################################
##### THE WEB PAGES THEMSELVES #####
####################################

class receive_message:

    def GET(self):
        return render.home()

    def POST(self):

        msg_args, num_args = parse_message()

        if num_args==2:
          inactivate_reminder(msg_args)

        # sender, name, msg [, interval [, repeats]]
        elif 2 < num_args <= 5:

            msg_args = add_defauts(msg_args)

            model.new_reminder(*msg_args)

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
