#!/usr/bin/env python3 

import time
import requests
import sys
import hashlib
import urllib.parse
sys.path[0:0] = ['../../']
import config as cfg

login_body = ('O=helpdesk.htm&usr=admin&pws=' + hashlib.md5(cfg.hub['pass'].encode('utf-8')).hexdigest())

# login to router
def login():
  print('logging in...')
  login = requests.post(cfg.hub['url'] + '/login.cgi', cookies=cfg.cookies, data=login_body, allow_redirects=False)
  time.sleep(1)

def getpi():
  print('getting pi')
  pi = requests.get(cfg.hub['url'] + '/cgi/renewPi.js', cookies=cfg.cookies)
  return(pi.text)

login()
pi = getpi()
print(pi)

delstring = ('CMD=&GO=my_network.htm&SET0='+ '50426637' + '%3Dd%252C' + 'DE%2533A49%2533AAE%2533AA9%2533A3D%2533A5F' + '%253B' + '&pi=' + pi)

#delstring2 = (urllib.parse.quote('CMD=&GO=my_network.htm&SET0=50426637=d,DE:49:AE:A9:3D:5F;' + '&pi=' + pi))
#print(delstring)
#print(delstring2)



delete = requests.post(cfg.hub['url'] + '/apply.cgi', cookies=cfg.cookies,  data=(delstring))
print(delete.request.headers)
print(delete.request.body)
print (delete.status_code)
print (delete.text)
