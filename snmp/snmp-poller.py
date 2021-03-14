#!/usr/bin/env python3 
import requests, urllib.parse, hashlib, sys, re

# read config from root directory
sys.path[0:0] = ['../']
import config as cfg

# body of login request
login_body = ('O=helpdesk.htm&usr=admin&pws=' + hashlib.md5(cfg.hub['pass'].encode('utf-8')).hexdigest())

# login request
def login():
  login_request = requests.post(cfg.hub['url'] + '/login.cgi', cookies=cfg.cookies, data=login_body, allow_redirects=False)

# request status page 
helpdesk_request = requests.get(cfg.hub['url'] + '/cgi/cgi_helpdesk.js', cookies=cfg.cookies, allow_redirects=False)

# if a 302 login
if (str(helpdesk_request.status_code) == '302'):
  login()
  helpdesk_request = requests.get(cfg.hub['url'] + '/cgi/cgi_helpdesk.js', cookies=cfg.cookies, allow_redirects=False)

# get helpdesk page content
content = helpdesk_request.content

# split content by ; 
vars = content.decode().split(";")

# decode vars from helpdesk
def helpdesk_parse(raw):
    line = raw.split('=')
    return(urllib.parse.unquote(line[1].strip().strip('".').strip('\'.')))

# split the event log var 
for var in vars:

  # remove line breaks
  var_o = var.strip('\r\n')

  # product name
  if ( re.search('product_name', var_o )):
       product_name = helpdesk_parse(var_o)

  if ( re.search('serial_no', var_o )):
       serial_no = helpdesk_parse(var_o)
#       print('serial_no:', serial_no)

  if ( re.search('fw_ver', var_o )):
       fw_ver = helpdesk_parse(var_o)
#       print('fw_ver:', fw_ver)

  # uptime
  if ( re.search('sysuptime', var_o )):
       sysuptime = str(helpdesk_parse(var_o) + '00')

#  print(var_o)

# open db file
db = open('smarthub.db', "w")

# sysDesc
db.write('1.3.6.1.2.1.1.1.0' + '_' + product_name + '-' + fw_ver.split(' ')[0] +'\n')

# device uptime
db.write('1.3.6.1.2.1.1.3.0' + '_' + sysuptime  + '\n')

# interface count
db.write('1.3.6.1.2.1.2.1.0' + '_' + str(len(cfg.snmp)) + '\n')

# device rates
# array of var?
vars = (requests.get(cfg.hub['url'] + '/cgi/cgi_basicMyDevice.js').content.decode()).split('var')

# array of 3rd var split by \n?
rate = vars[2].split('\n')

for rate in rate:
 # fix rate line?
 rate = urllib.parse.unquote(rate.replace('\'', ''))

 # get rate items
 rate_items = rate.split(',')

 # mac bw lines start with timestamp
 if ( re.search('timestamp', rate_items[0])):

    # mac address
    mac = (rate_items[2].replace('mac:', '')).upper()

    # search for macs in the cfg file
    try:

      # interface no and name
      int_no =  (cfg.snmp[mac])[0]
      int_name =  (cfg.snmp[mac])[1]

      tx = (rate_items[3].replace('tx:', ''))
      rx = (rate_items[4].replace('rx:', ''))
      rx = rx.replace('}','')

      # int name
      db.write('1.3.6.1.2.1.2.2.1.2.' + int_no + '_' + int_name + '\n')
      # int uptime ( system uptime ) 
      db.write('1.3.6.1.2.1.2.2.1.9.' + int_no + '_' + sysuptime + '\n')
      # int rx
      db.write('1.3.6.1.2.1.2.2.1.10.' + int_no + '_' + rx + '\n')
      # int rx
      db.write('1.3.6.1.2.1.2.2.1.16.' + int_no + '_' + tx + '\n')

    except KeyError:
      pass

#  close
db.close()
