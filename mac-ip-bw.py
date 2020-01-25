#!/usr/bin/env python3 

import requests
import urllib.parse
import sys
import re
# local config
import config as cfg

# request page
vars = (requests.get(cfg.hub['url'] + '/cgi/cgi_basicMyDevice.js').content.decode()).split('var')

known_device_list = vars[1].split('\n')
rate = vars[2].split('\n')

# store mac to ip mappings
mac_to_ip = {}

# get device list
for device in known_device_list:

    device = urllib.parse.unquote(device.replace('\'', ''))
    device_items = device.split(',')
    mac = device_items[0]

    # fix for the first mac address
    if (re.search('known_device_list', mac)):
       mac = mac.replace('known_device_list=[', '')

    mac_f = mac.split('{mac:')
    try:
      mac_addr = mac_f[1]
    except:
      continue

    ip = device_items[2]
    ip_addr = ip.split('ip:')
    mac_to_ip[mac_addr] = ip_addr[1]

for rate in rate:
  rate = urllib.parse.unquote(rate.replace('\'', ''))
  rate_items = rate.split(',')
  if ( re.search('timestamp', rate_items[0])):
      rate_mac = (rate_items[2].replace('mac:', '')).upper()
      tx = (rate_items[3].replace('tx:', ''))
      rx = (rate_items[4].replace('rx:', ''))
      rx = rx.replace('}','')
      try:
        if (mac_to_ip[rate_mac]):
          print(rate_mac, mac_to_ip[rate_mac], tx, rx)
      except:
        continue
