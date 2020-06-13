# btsmarthub-utils

scripts / container that poll the BT Smart Hub 2 to get logs and internet usage per device

the logs and data can also be exported to syslog / graphite

New: a script to delete devices from the smarthub

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

* delete a device from the smarthub from the command line

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

# misc smarthub info that may save you some time

I spent a few hours diagnosing why some bridge interfaces on my homelab virtualisation setup were showing dropped RX packets. I initally suspected some powerline adapters; but it turned out to be the smarthub doing this kind of thing..

```
12:38:45.723880 64:cc:22:00:b9:fd (oui Unknown) > 01:80:c2:ef:03:fe (oui Unknown), ethertype Unknown (0xfe68), length 102:
	0x0000:  0303 0485 36ec 00c0 0180 c2ef 03fe 64cc  ....6.........d.
	0x0010:  2200 b9fd 0d36 4458 0303 0d85 36ec 00c0  "....6DX....6...
	0x0020:  8c51 218a 0b98 d6a0 e2dd 7347 8c51 2950  .Q!.......sG.Q)P
	0x0030:  57f1 d830 c222 7e41 d209 e1ab 1af5 7aae  W..0."~A......z.
	0x0040:  7761 7459 3c20 e7c3 7b9c c94c 5a51 276c  watY<...{..LZQ'l
	0x0050:  62a9 42e8 41e6 ef72                      b.B.A..r
```

I guess its something to do with whole home wifi discs. I ended up using nftables to drop them eg: 

```
#!/usr/sbin/nft -f

flush ruleset

table netdev filter {
    chain ingress {
    type filter hook ingress device enp0s25 priority 0; policy accept;
        meta protocol 0xfe68  drop
    }
}
```
