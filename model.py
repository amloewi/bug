import web
import time

#Connection URL:
#    postgres://saacaqioxidlzo:uTBA7xiv_GqC99oNQCf4R5FzFo@ec2-54-83-23-169.compute-1.amazonaws.com:5432/dqskbvn58g0hu
db = web.database(dbn='postgres',
                    user='saacaqioxidlzo',
                    pw='uTBA7xiv_GqC99oNQCf4R5FzFo',
                    host='ec2-54-83-23-169.compute-1.amazonaws.com',
                    port=5432,
                    db='dqskbvn58g0hu',
                    sslmode='require')


def new_reminder(number, name, msg, interval, repeats):
    interval_in_seconds = interval*60
    now = int(time.time())
    db.insert('reminders',
                name=name,
                sender_number=number,
                message=msg,
                interval=interval_in_seconds,
                send_at=now+interval_in_seconds,
                times_sent=0,
                repeats_left=repeats,
                time_set=now,
                time_done=-1)

def inactivate_reminder(name):
    # WHAT IF THERE ARE MORE THAN ONE ACTIVE WITH THE SAME NAME?
    # Fuck it.
    r = db.where('reminders', name=name)[0]
    r['repeats_left']=0
    r['time_done'] = int(time.time())
    db.insert('reminders', **r)

def get_active():
    active = list(db.query("SELECT * FROM reminders WHERE repeats_left!=0"))
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
#   time_done bigint
# );
