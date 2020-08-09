#!/usr/bin/env python3 

import requests, re, sys
import urllib.parse
import hashlib
sys.path[0:0] = ['../']
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
r = requests.get(cfg.hub['url'] + '/cgi/cgi_broadband.js?', cookies=cfg.cookies, allow_redirects=False)

# if a 302 login
if (str(r.status_code) == '302'):
  login()
  r = requests.get(cfg.hub['url'] + '/cgi/cgi_broadband.js?', cookies=cfg.cookies, allow_redirects=False)

content = r.content
vars = content.decode().split(";")
count=0

# split the event log var 
for var in vars:
  var_o = var.strip('\r\n')
  var_o = str(var_o.replace('\n', ''))
  var_list = var_o.split(",")
  stats = var_list[0].split("=")
  value = str(stats[1].replace("'", ''))
  stat = str(stats[0].replace('var ', ''))
  stat = str(stat.replace(' ', ''))
  count += 1
  if (count > 10):
    break

  if (re.search('internet', stat) and (str(value) == '1')):
    print('broadband is', print_c('green', 'ONLINE'))
  if (re.search('wan_link_rate_list', stat)):
    print('broadband speed', print_c('green', var_o))
