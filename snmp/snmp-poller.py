#!/usr/bin/env python3 

import requests, urllib.parse, hashlib, sys, re

sys.path[0:0] = ['../']
import config as cfg

# body of login request
login_body = ('O=helpdesk.htm&usr=admin&pws=' + hashlib.md5(cfg.hub['pass'].encode('utf-8')).hexdigest())

def login():
  login = requests.post(cfg.hub['url'] + '/login.cgi', cookies=cfg.cookies, data=login_body, allow_redirects=False)

# request status page 
r = requests.get(cfg.hub['url'] + '/cgi/cgi_helpdesk.js', cookies=cfg.cookies, allow_redirects=False)

# if a 302 login
if (str(r.status_code) == '302'):
  login()
  r = requests.get(cfg.hub['url'] + '/cgi/cgi_helpdesk.js', cookies=cfg.cookies, allow_redirects=False)

content = r.content

# split content by ; 
vars = content.decode().split(";")

# decode vars from helpdesk
def get_var1(raw):
    line = raw.split('=')
    return(urllib.parse.unquote(line[1].strip().strip('".').strip('\'.')))

# split the event log var 
for var in vars:

  # remove line breaks
  var_o = var.strip('\r\n')
  if ( re.search('product_name', var_o )):
       product_name = get_var1(var_o)
#       print('product_name:', product_name)

  if ( re.search('serial_no', var_o )):
       serial_no = get_var1(var_o)
#       print('serial_no:', serial_no)

  if ( re.search('fw_ver', var_o )):
       fw_ver = get_var1(var_o)
#       print('fw_ver:', fw_ver)

  if ( re.search('sysuptime', var_o )):
       sysuptime = get_var1(var_o)
#       print('sysuptime:', sysuptime)

#  print(var_o)

print('1.3.6.1.2.1.1.1.0' + ':' + product_name + '-' + fw_ver.split(' ')[0])
print('1.3.6.1.2.1.1.3.0' + ':' + sysuptime)
