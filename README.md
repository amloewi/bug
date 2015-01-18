bug
===

An insistent SMS-based reminder service.

The input string for bug is:

**\<name of job\>, \<reminder message\>, [, \<number of minutes between reminders\> [, \<times message will be sent\> ]]**
With defaults on the last two, optional parameters being 30 minutes between reminders, and 5 repeated messages.

Ex: Food, Go buy food!, 30, 4 # The job named "Food" will send you the message "Go buy food! 4 times, 30 minutes apart.

Ex: Call, Call Shelly # The job named "Call" will send you the message "Call Shelly" 5 times, 30 minutes apart, because those are the defaults on the paramaters.

The name of the job is meant as an identifier by which the job can be cancelled, with 'Did \<job\>' but that feature has not yet been implemented.
