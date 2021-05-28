#!/usr/bin/env python3

import requests,re,sys,hashlib
import urllib.parse
sys.path[0:0] = ['../']
import config as cfg


def login():
  login_body = ('O=helpdesk.htm&usr=admin&pws=' + hashlib.md5(cfg.hub['pass'].encode('utf-8')).hexdigest())
  login = requests.post(cfg.hub['url'] + '/login.cgi', cookies=cfg.cookies, data=login_body, allow_redirects=False)

# request status page
def cgi_broadband():
  return(requests.get(cfg.hub['url'] + '/cgi/cgi_broadband.js?', cookies=cfg.cookies, allow_redirects=False))

# if a 302 login
r = cgi_broadband()
if (str(r.status_code) == '302'):
  login()
  r = cgi_broadband()

content = r.content
vars = content.decode().split(";")

count=0

# https://stackoverflow.com/questions/12523586/python-format-size-application-converting-b-to-kb-mb-gb-tb
# changed to 1000 for the smarthub
def humanbytes(B):
   'Return the given bytes as a human friendly KB, MB, GB, or TB string'
   B = float(B)
   KB = float(1000)
   MB = float(KB ** 2) # 1,048,576
   GB = float(KB ** 3) # 1,073,741,824
   TB = float(KB ** 4) # 1,099,511,627,776

   if B < KB:
      return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
   elif KB <= B < MB:
      return '{0:.2f} KB'.format(B/KB)
   elif MB <= B < GB:
      return '{0:.2f} MB'.format(B/MB)
   elif GB <= B < TB:
      return '{0:.2f} GB'.format(B/GB)
   elif TB <= B:
      return '{0:.2f} TB'.format(B/TB)

# split the event log var
for var in vars:
  var_o = var.strip('\r\n')
  var_o = str(var_o.replace('\n', ''))
  var_list = var_o.split(",")
  stats = var_list[0].split("=")
  value = str(stats[1].replace("'", ''))
  stat = str(stats[0].replace('var ', ''))
  stat = str(stat.replace(' ', ''))

  # counter
  count += 1
  if (count > 10):
    break

  if (re.search('wan_link_rate_list', stat)):
    link = (var_o.split("'")[3]).split("%3B")
    upload = humanbytes(int(link[0]))
    download = humanbytes(int(link[1]))
    print("rate:  " + download + " down " + upload + " up")

  if (re.search('wan_conn_volume_list', stat)):
    bw = (var_o.split("'")[3]).split("%3B")
    total = humanbytes(int(bw[0]))
    download = humanbytes(int(bw[1]))
    upload = humanbytes(int(bw[2]))
    print("usage: " + total + " total (" + download + " down " + upload +" up)")
