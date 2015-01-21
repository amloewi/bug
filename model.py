import web
import time
import os

JOB_NAMES = ["ant", "beetle", "cicada"]#, "", "beetle"]
NUM_NAMES = len(JOB_NAMES)

# Chooses the correct database connection based upon whether the db is local,
# and for development, or the actual site's db. Does so by testing the path
# of the current file.
if os.path.abspath("") == '/Users/alexloewi/Documents/Sites/bug':
  db = web.database(dbn='postgres',
            user='alexloewi',
            pw='dian4nao3',
            db='alexloewi')
else:
  #Connection URL:
  #    postgres://saacaqioxidlzo:uTBA7xiv_GqC99oNQCf4R5FzFo@ec2-54-83-23-169.compute-1.amazonaws.com:5432/dqskbvn58g0hu
  db = web.database(dbn='postgres',
                      user='saacaqioxidlzo',
                      pw='uTBA7xiv_GqC99oNQCf4R5FzFo',
                      host='ec2-54-83-23-169.compute-1.amazonaws.com',
                      port=5432,
                      db='dqskbvn58g0hu',
                      sslmode='require')




def new_reminder(sender, msg, interval, repeats):
    interval_in_seconds = interval*60
    now = int(time.time())
    active = len(list(db.where('reminders', sender_number=sender)))

    # This assigns job names from the list of names
    # above. If the number of active jobs goes over 5,
    # it starts to append digits to the job string,
    # i.e. ant1, fly1, etc.
    name = JOB_NAMES[active%NUM_NAMES]
    if active/NUM_NAMES:
      name += str(active/NUM_NAMES)

    db.insert('reminders',
                name=name,
                sender_number=sender,
                message=msg,
                interval=interval_in_seconds,
                send_at=now+interval_in_seconds,
                times_sent=0,
                repeats_left=repeats,
                time_set=now,
                time_done=-1)

    return sender, name


def inactivate_reminder(sender, name, msg_type):
    """Called by the sweep, for run-out messages, and by 'did' and 'cancel' msgs

    """

    r = list(db.where('reminders',
                      name=name.strip(),
                      sender_number=sender))
    if r:
      r = r[0]
    else:
      return None, None

    # Take it out of the old table no matter what.
    db.delete('reminders', where="id=$id", vars=r)

    if msg_type != "cancel": #It was "did" or "ran_out"
      r['time_done'] = int(time.time())
      # If not "did", it was "ran_out"
      r['completed'] = True if msg_type == "did" else False
      db.insert('old_reminders', **r)

    return sender, name.strip()



def get_active():
    active = list(db.query("SELECT * FROM reminders"))# WHERE repeats_left!=0"))
    return active


def reinsert(reminder):
    db.update('reminders', where="id=$id", vars=reminder, **reminder)


# --
# create table reminders(
#   -- A SHORT code used to identify the reminder, and turn it off.
#   -- 'Did *name*' will stop the remaining messages.
#   name char(20),
#   -- The message itself, sent to the user in the reminder text.
#   message char(200),
#   -- The number of seconds in between reminders
#   interval smallint,
#   -- The time (in seconds since 1970) at which to send the next reminder
#   send_at bigint,
#   -- The number of times the message has been sent so far
#   repeated int,
#   -- The number of times the message will be repeated in the future
#   -- Set to '-1' for indefinitely repeating
#   -- COULD be used as 'if repeats_left != 0' for 'active' ... speed?
#   repeats_left smallint,
#   -- Whether or not there are repeats left
#   -- active boolean,
#   time_set bigint,
#   time_done bigint,
#   completed boolean
# );
