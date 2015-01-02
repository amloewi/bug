--
create table reminders(
  id serial primary key,
  -- A SHORT code used to identify the reminder, and turn it off.
  -- 'Did *name*' will stop the remaining messages.
  name char(20),
  -- The phone number of the sender, as a string
  sender_number char(12), -- "+1 503 274 7031" (without spaces) is twelve chars
  -- The message itself, sent to the user in the reminder text.
  message char(200),
  -- The number of seconds in between reminders
  interval smallint,
  -- The time (in seconds since 1970) at which to send the next reminder
  send_at bigint,
  -- The number of times the message has been sent so far
  times_sent int,
  -- The number of times the message will be repeated in the future
  -- Set to '-1' for indefinitely repeating
  -- COULD be used as 'if repeats_left != 0' for 'active' ... speed?
  repeats_left smallint,
  -- Whether or not there are repeats left
  -- active boolean,
  time_set bigint,
  time_done bigint
);

create table old_reminders () inherits (reminders);
