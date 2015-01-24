bug
===

An insistent SMS-based reminder service.

A better introduction to **bug** can be found at http://sikeda.herokuapp.com

The input string for bug is:

**\<message\> [ \<minutes between reminders=30\> [ \<times message will be sent=5\> ]]**

Meaning the last two parameters are optional, and have defaults of 30 minutes between reminders, and 5 repeated messages. The parameters need to be separated by spaces, and if you have a number at the end of your message,
you need to include punctuation to show it's not a parameter. E.g. "Dinner at 8" will think '8' is the interval, but "Dinner at 8." with the period will work fine.

**Ex:** *Go buy food! 60 4* # You will get the message "Go buy food! 4 times, 60 minutes apart.

**Ex:** *Call Shelly* # You will get the message "Call Shelly" 5 times, 30 minutes apart, because those are the defaults on the parameters.

When you make a reminder you will receive a text telling you what the name of your reminder is. You can use this to stop the messages when you finish the thing you wanted to do, or to cancel them if you made a mistake, with

**Cancel/Did \<reminder name\>**
