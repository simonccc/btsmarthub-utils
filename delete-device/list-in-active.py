#!/usr/bin/env python3 

import requests
import urllib.parse
import re
import sys
sys.path[0:0] = ['../']
import config as cfg

# request page
r = requests.get(cfg.hub['url']+ '/cgi/cgi_basicMyDevice.js')

def print_c(color, string):
  if cfg.tail_colors['enabled'] == 'true':
   return(cfg.tail_colors[color] + string  + '\x1b[0m ')
  else:
   return(string)

content = r.content
mac_c = 1
vars = content.decode().split("\n")

for var in vars:
    var_types = var.split(",")

    # fix for the first mac address
    if (re.search('var known_device_list', var_types[0])):
       var_types[0] = var_types[0].replace('var known_device_list=[', '')
    var_types[0] = var_types[0].replace('{', '')
    var_types[0] = var_types[0].replace('\'', '')

    try:
      mac = urllib.parse.unquote(var_types[0].split(":")[1])
      rmac = var_types[0].split(":")[1]
      rmac2 = rmac.replace('%3A', '%253A')
    except:
     continue 

    try:
      macf = urllib.parse.unquote(var_types[0].split(":")[0])
      if (re.search('mac', macf)):
        pass
      else:
        continue
    except:
     pass 

    try: 
      hostname = urllib.parse.unquote(var_types[1].split(":")[1]).replace('\'', '')
    except:
     continue
    try:
      name = urllib.parse.unquote(var_types[4].split(":")[1]).replace('\'', '')
    except:
      continue
    try: 
      os = urllib.parse.unquote(var_types[6].split(":")[1]).replace('\'', '')
    except:
      continue
    device = urllib.parse.unquote(var_types[7].split(":")[1]).replace('\'', '')
    if (hostname == '' ):
        hostname = name
    if (re.search('unknown_', hostname)):
        hostname = os
    if (re.search('Unknown', hostname)):
        hostname = device
    ip = urllib.parse.unquote(var_types[2].split(":")[1]).replace('\'', '')
    activity = urllib.parse.unquote(var_types[5].split(":")[1])
    mac_c = (int(mac_c) + 1)

    if (activity == '\'1\'' ):
       continue
    os = urllib.parse.unquote(var_types[6].split(":")[1])
    active = urllib.parse.unquote(var_types[9].split(":")[1]).replace('\'', '')
    port = urllib.parse.unquote(var_types[11].split(":")[1]).replace('\'', '')

#    print(str(mac_c) + ' ' + mac,rmac2,ip, hostname, active)
    print(active,hostname,ip,mac)

