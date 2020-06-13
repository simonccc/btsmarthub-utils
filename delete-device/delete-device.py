#!/usr/bin/env python3

import datetime, re, requests, hashlib, sys

# check for mac
if len(sys.argv) < 2:
    print (sys.argv[0], 'mac:addr')
    exit(1)

# encode mac addr
mac=re.sub(':', '%253A', sys.argv[1])

# load cfg
sys.path[0:0] = ['../']
import config as cfg

# login
login_body = ('O=helpdesk.htm&usr=admin&pws=' + hashlib.md5(cfg.hub['pass'].encode('utf-8')).hexdigest())
login = requests.post(cfg.hub['url'] + '/login.cgi', cookies=cfg.cookies, data=login_body)

# get pi and current ts
pi = requests.get(cfg.hub['url'] + '/cgi/renewPi.js', cookies=cfg.cookies).text
ts = int(datetime.datetime.now().strftime('%s%f')[:-3])

# get cfg id for updating known devices list
n = requests.get(cfg.hub['url'] + '/cgi/cgi_myNetwork.js?ts=' + str(ts)).text
for line in n.splitlines():
    if re.search('known_devices_update', line):
        cfg_id = line.split(',')[1]

# prepare the post body and header
delstring = ('CMD=&GO=my_network.htm&SET0='+ cfg_id + '%3Dd%252C' + mac + '%253B' + '&pi=' + pi)

# send delete request
delete = requests.post(cfg.hub['url'] + '/apply.cgi', data=(delstring), cookies=cfg.cookies)
print (delete.status_code)
