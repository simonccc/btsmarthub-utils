# btsmarthub-utils

* scrape the logs displayed in the gui and tail them in the console or send to syslog

* poll the internet usage for devices connected and send the metrics to graphite 

* docker image to ease deployment

# manual setup

python3 

`pip3 install -r requirements.txt`

copy `example-config.py` to `config.py` and edit it

'hub' are the smarthub details

'logger' are the syslog server details

'colors' to change or disable colors

'cookies' is used for logging in to the router; urn is just a random thing - can be changed if required

'graphite' graphite server and prefix for the smarthub data

# cli tools

* logs-tail.py - tails the log to stdout with colors

* logs-syslog.py - send's the logs to a remote syslog server ( only tested with logstash ) 

* bandwidth-graphite.py - sends bandwidth info per mac addr to graphite

see misc for other small unfinished things that may be useful

# docker 

See the docker file and scripts and examples to build a docker image to run the syslog and graphite script
