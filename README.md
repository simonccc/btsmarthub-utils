# btsmarthub-utils

* scrape the logs displayed in the normal gui and tail -f them in the console or send to syslog

* poll the internet usage for devices connected and send the metrics to graphite

* other random stuff

# setup

copy `example-config.py` to `config.py` and edit it

```
'hub' is the smarthub name eg smarthub.home or IP address
'logger' syslog server name/IP:port
'colors' to change or disable colors in the tail like output
'cookies' urn is a random string used in requests
'graphite' graphite server and prefix for the smarthub data ( only tested on port 2003 ) 
```

# docker 

`docker pull simonczuzu/btsmarthub-utils`

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

