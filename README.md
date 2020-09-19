# btsmarthub-utils

scripts / container that poll the BT Smart Hub 2 to get logs and internet usage per device

the logs and data can also be exported to syslog / graphite

tested against:

```
product_name    "HomeHub6DX"

fw_ver "v0.21.03.07094-BT (Thu Jul  9 17:43:55 2020)"

board_ver  "R01"
gui_ver  "1.56 15_02_2019"
boot_ver    " 0.1.7-BT (Thu Nov 30 09:45:22 2017)"

```
see the pre0.21 branch for support for older versions 


# Features

* scrape the logs displayed in the normal gui and tail -f them in the console or send to syslog

* poll the internet usage for mac addresses connected and send the metrics to graphite

* docker image to ease deployment

* see delete-device dir for a script to delete inactive devices

# manual setup

python3 

`pip3 install -r requirements.txt`

copy `example-config.py` to `config.py` and edit it

```
'hub' is the smarthub name eg smarthub.home or IP address
'logger' syslog server name/IP:port
'colors' to change or disable colors in the tail like output
'cookies' urn is a random string used in requests
'graphite' graphite server and prefix for the smarthub data ( only tested on port 2003 ) 
```

# cli tools

```
* logs-tail.py - tails the log to stdout with colors
* logs-syslog.py - send's the logs to a remote syslog server ( only tested with logstash ) 
* bandwidth-graphite.py - sends bandwidth info per mac addr to graphite
* delete-device/ - scripts for deleting inactive devices
* misc/ other small unfinished things that may be useful
```

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

