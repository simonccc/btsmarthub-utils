# btsmarthub-utils

Some scripts and a docker container that poll the BT Smart Hub 2 to get the logs and internet usage per device and export them to syslog and graphite. 

I've only tested against this combo: 
```
product_name    "HomeHub6DX"
fw_ver  "v0.16.02.08304-BT (Fri Aug 30 17:58:36 2019)"
board_ver  "R01"
gui_ver  "1.56 15_02_2019"
```

# Features 

* scrape the logs displayed in the normal gui and tail -f them in the console or send to syslog

* poll the internet usage for mac addresses connected and send the metrics to graphite 

* docker image to ease deployment 

# manual setup

python3 

`pip3 install -r requirements.txt`

copy `example-config.py` to `config.py` and edit it

'hub' are the smarthub details

'logger' are the syslog server details

'colors' to change or disable colors in the tail like output 

'cookies' is used for logging in to the router; urn is just a random thing - can be changed if required

'graphite' graphite server and prefix for the smarthub data ( only tested on port 80 / http ) 

# cli tools

* logs-tail.py - tails the log to stdout with colors

* logs-syslog.py - send's the logs to a remote syslog server ( only tested with logstash ) 

* bandwidth-graphite.py - sends bandwidth info per mac addr to graphite

see misc for other small unfinished things that may be useful

# docker 

`docker pull simonczuzu/btsmarthub-utils`

or build the image locally using the script

example docker-compose file

```yml
version: '3'

services:
    smarthub:
      image: smarthub
      container_name: smarthub
      restart: unless-stopped
      hostname: smarthub
      environment:
        - DEBUG=yes
        - URL=http://smarthub
        - SMARTHUB_NAME=smarthub
        - PASS=password
        - LOGHOST=loghost
        - LOGHOST_PORT=514
        - G_HOST=graphitehost
        - G_PREFIX=smarthub
```
setting DEBUG sends the logs and metrics reports / data to stderr
