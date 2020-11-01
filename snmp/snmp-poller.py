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

  # product name
  if ( re.search('product_name', var_o )):
       product_name = get_var1(var_o)

  if ( re.search('serial_no', var_o )):
       serial_no = get_var1(var_o)
#       print('serial_no:', serial_no)

  if ( re.search('fw_ver', var_o )):
       fw_ver = get_var1(var_o)
#       print('fw_ver:', fw_ver)

  # uptime
  if ( re.search('sysuptime', var_o )):
       sysuptime = str(get_var1(var_o) + '00')

#  print(var_o)

# open db file
db = open('smarthub.db', "w")

# sysDesc
db.write('1.3.6.1.2.1.1.1.0' + '_' + product_name + '-' + fw_ver.split(' ')[0] +'\n')

# device uptime
db.write('1.3.6.1.2.1.1.3.0' + '_' + sysuptime  + '\n')

# device rates
vars = (requests.get(cfg.hub['url'] + '/cgi/cgi_basicMyDevice.js').content.decode()).split('var')
rate = vars[2].split('\n')

# define devices
my_devices = {
        "3C:97:0E:0A:AC:90": [ '1', 'leno' ]
        }

for rate in rate:
 rate = urllib.parse.unquote(rate.replace('\'', ''))
 rate_items = rate.split(',')

 # mac bw lines start with timestamp
 if ( re.search('timestamp', rate_items[0])):
    rate_mac = (rate_items[2].replace('mac:', '')).upper()

    try:
      device =  my_devices[rate_mac]
      tx = (rate_items[3].replace('tx:', ''))
      rx = (rate_items[4].replace('rx:', ''))
      rx = rx.replace('}','')
      db.write('1.3.6.1.2.1.2.2.1.2.' + device[0] + '_' + device[1] + '\n')

      leno_tx = (tx)
      leno_rx = (rx)
    except KeyError:
      pass

# int 1
db.write('1.3.6.1.2.1.2.2.1.9.1' + '_' + sysuptime + '\n')
db.write('1.3.6.1.2.1.2.2.1.10.1' + '_' + leno_rx + '\n')
db.write('1.3.6.1.2.1.2.2.1.16.1' + '_' + leno_tx + '\n')

db.close()
