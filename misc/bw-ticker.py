#!/usr/bin/env python3

import requests,re,sys,hashlib,time
import urllib.parse
sys.path[0:0] = ['../']
import config as cfg

def login():
  login_body = ('O=helpdesk.htm&usr=admin&pws=' + hashlib.md5(cfg.hub['pass'].encode('utf-8')).hexdigest())
  login = requests.post(cfg.hub['url'] + '/login.cgi', cookies=cfg.cookies, data=login_body, allow_redirects=False)

# request status page
def cgi_broadband():
  return(requests.get(cfg.hub['url'] + '/cgi/cgi_broadband.js?', cookies=cfg.cookies, allow_redirects=False))

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
      return '{0:.3f} KB'.format(B/KB)
   elif MB <= B < GB:
      return '{0:.3f} MB'.format(B/MB)
   elif GB <= B < TB:
      return '{0:.3f} GB'.format(B/GB)
   elif TB <= B:
      return '{0:.3f} TB'.format(B/TB)

def start():
  r = cgi_broadband()
  if (str(r.status_code) == '302'):
    login()
  return(cgi_broadband())

old_ticker = 0

# init
while True:
  r = start()
  content = r.content
  vars = content.decode().split(";")

  # split the event log var
  for var in vars:
    var_o = var.strip('\r\n')
    var_o = str(var_o.replace('\n', ''))
    var_list = var_o.split(",")
    stats = var_list[0].split("=")
    value = str(stats[1].replace("'", ''))
    stat = str(stats[0].replace('var ', ''))
    stat = str(stat.replace(' ', ''))

    if (re.search('wan_conn_volume_list', stat)):
      bw = (var_o.split("'")[3]).split("%3B")
      ticker =  "total " + humanbytes(int(bw[0])) + " (" + humanbytes(int(bw[1])) + " D " + humanbytes(int(bw[2])) +" U)"
      if ( ticker != old_ticker ):
        print(ticker)
        old_ticker = ticker
        break

  #    print('no ' + ticker)
      break
  #  print(',')

  # sleep
  time.sleep(5)
