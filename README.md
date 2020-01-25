# btsmarthub-utils

Utilities for working with the BT Smarthub 2

# setup

python3 

`pip3 install -r requirements.txt`

copy `example-config.py` to `config.py` and edit it

'hub' are the smarthub details
'logger' are the syslog server details
'colors' to change or disable colors
'cookies' is used for logging in to the router - change 'urn' if you want
'graphite' graphite server and prefix 

# features

* logs-tail.py - tails the log to stdout with colors

* logs-syslog.py - send's the logs to a remote syslog server ( only tested with logstash ) 

* list-active.py - lists active clients on the network

* logout.py - logs you out of the router

* mac-ip-bw.py - displays the macs and current map'd IP's and raw bw stats

* bwmon.py - sends bandwidth info per mac addr to graphite
