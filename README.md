# btsmarthub-utils

* [logs-tail](logs-tail) - scrape the logs displayed in the normal gui and tail -f them in the console or send to syslog

* [bandwidth-graphite](bandwidth-graphite) - poll the internet usage for devices connected and send the metrics to graphite

* [delete-device](delete-device) - delete device from the smarthubs db via mac address

* [docker](docker) docker version - supports syslog output

* [misc](misc) much non working stuff

# setup

copy `example-config.py` to `config.py` and edit it

```
'hub' is the smarthub name eg smarthub.home or IP address
'logger' syslog server name/IP:port
'colors' to change or disable colors in the tail like output
'cookies' urn is a random string used in requests
'graphite' graphite server and prefix for the smarthub data ( only tested on port 2003 ) 
```
