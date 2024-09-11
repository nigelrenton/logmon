# logmon

logmon processes log files and performs an alert if all predefined conditions are matched.
Intended to run as a service on Debian 12.

#### jobs.py

```
jobs = [ # a python list of dictionaries 
#    {
#        'log': '/path/to/file.log',                                             # path to log file to monitor
#        'conditions': ['FAILED', 'ce:c0:3b:f0:3d:18', 'DHCP'],                  # list of strings in loog line to match, case sensitive
#        'no_repeat': 0,                                                         # time in minutes to ignore reoccurence of conditions
#        'alerts': ['email', 'console'],                                         # list of actions to perform if conditions are matched 'email' 'console'...
#        'email_recipients': ["example@nigel.net", "example@renton.org"]         # list of email recipients if 'email' is alert type
#    }
```

