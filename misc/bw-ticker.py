#!/usr/bin/env python3

import requests,re,sys,hashlib,time,urllib.parse
sys.path[0:0] = ['../']
import config as cfg

def login():
  login_body = ('O=helpdesk.htm&usr=admin&pws=' + hashlib.md5(cfg.hub['pass'].encode('utf-8')).hexdigest())
  login = requests.post(cfg.hub['url'] + '/login.cgi', cookies=cfg.cookies, data=login_body, allow_redirects=False)

# request status page
def cgi_broadband():
  return(requests.get(cfg.hub['url'] + '/cgi/cgi_broadband.js?', cookies=cfg.cookies, allow_redirects=False))

def print_c(color, string):
  if cfg.tail_colors['enabled'] == 'true':
   return(cfg.tail_colors[color] + string  + '\x1b[0m ')
  else:
   return(string)

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
      return '{0:.5f} GB'.format(B/GB)
   elif TB <= B:
      return '{0:.6f} TB'.format(B/TB)

def get_data():
  if (str(cgi_broadband().status_code) == '302'):
    login()
  content = cgi_broadband().content
  return(content.decode().split(";"))

old_ticker = 0
old_total = 0
old_download = 0
old_upload = 0

# init
while True:

  # split the event log var
  for var in get_data():
    if (re.search('wan_conn_volume_list', var)):
      bw = (var.split("'")[3]).split("%3B")

      total = humanbytes(int(bw[0]))
      download = humanbytes(int(bw[1]))
      upload = humanbytes(int(bw[2]))

      ticker =  total + "," + download + "," + upload
      if ( ticker != old_ticker ):
        print(print_c('yellow','total:') ,end ='')

        if ( total != old_total ):
            print(print_c('blue',total) , end ='')
        if ( total == old_total ):
            print(total + " ", end ='')

        print(print_c('yellow','download:') ,end ='')

        if ( download != old_download ):
            print(print_c('green',download) , end ='')
        if ( download == old_download ):
            print(download + " ", end ='')

        print(print_c('yellow','upload:') ,end ='')

        if ( upload != old_upload ):
            print(print_c('red',upload) , end ='')
        if ( upload == old_upload ):
            print(upload, end ='')

        print()

        old_ticker = ticker
        old_total = total
        old_download = download
        old_upload = upload
        break

      print('no ' + ticker)
      break
  #  print(',')

  # sleep
  time.sleep(10)
