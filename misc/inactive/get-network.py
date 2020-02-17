#!/usr/bin/env python3 

import time
import requests
import sys
import hashlib
sys.path[0:0] = ['../../']
import config as cfg

login_body = ('O=helpdesk.htm&usr=admin&pws=' + hashlib.md5(cfg.hub['pass'].encode('utf-8')).hexdigest())

# login to router
def login():
  print('logging in...')
  login = requests.post(cfg.hub['url'] + '/login.cgi', cookies=cfg.cookies, data=login_body, allow_redirects=False)
  time.sleep(1)

login()
n = requests.get(cfg.hub['url'] + '/cgi/cgi_myNetwork.js?4', cookies=cfg.cookies)
print(n.text)
