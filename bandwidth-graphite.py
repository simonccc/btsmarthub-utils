#!/usr/bin/env python3

import requests
import urllib.parse
import re
import time
# local config
import config as cfg
import graphyte

graphyte.init(cfg.graphite['g_host'], prefix=cfg.graphite['prefix'], interval=20 )

while 1:

 # request page
 vars = (requests.get(cfg.hub['url'] + '/cgi/cgi_basicMyDevice.js').content.decode()).split('var')
 rate = vars[2].split('\n')

 for rate in rate:
  rate = urllib.parse.unquote(rate.replace('\'', ''))
  rate_items = rate.split(',')
  if ( re.search('timestamp', rate_items[0])):
     rate_mac = (rate_items[2].replace('mac:', '')).upper()
     tx = (rate_items[3].replace('tx:', ''))
     rx = (rate_items[4].replace('rx:', ''))
     rx = rx.replace('}','')
     graphyte.send(rate_mac + '.' + 'tx',int(tx))
     graphyte.send(rate_mac + '.' + 'rx',int(rx))

 time.sleep(10)
