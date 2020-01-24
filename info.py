#!/usr/bin/env python3 

import requests
import time
import datetime
import socket
import urllib.parse
import hashlib
import sys
import math
# local config
import config as cfg

# body of login request
login_body = ('O=helpdesk.htm&usr=admin&pws=' + hashlib.md5(cfg.hub['pass'].encode('utf-8')).hexdigest())

def login():
  print(print_c('red', 'logging in...'))
  login = requests.post(cfg.hub['url'] + '/login.cgi', cookies=cfg.cookies, data=login_body, allow_redirects=False)

def print_c(color, string):
  if cfg.tail_colors['enabled'] == 'true':
   return(cfg.tail_colors[color] + string  + '\x1b[0m ')
  else:
   return(string)


# request status page 
r = requests.get(cfg.hub['url'] + '/cgi/cgi_helpdesk.js', cookies=cfg.cookies, allow_redirects=False)

  # if a 302 login
if (str(r.status_code) == '302'):
  login()
  r = requests.get(cfg.hub['url'] + '/cgi/cgi_helpdesk.js', cookies=cfg.cookies, allow_redirects=False)

content = r.content
vars = content.decode().split(";")
count=0

# split the event log var 
for var in vars:
  var_o = var.strip('\r\n')
  var_list = var_o.split(",")
  try:
    if var_list[1]:
      continue
  except:
#    print(var_list[0])
    stats = var_list[0].split("=")
    if stats[1] == "":
        continue
    print(print_c('green',stats[0]), print_c('yellow', urllib.parse.unquote(stats[1])))
    count += 1
    if (count > 22):
      break

