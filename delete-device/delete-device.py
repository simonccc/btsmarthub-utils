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
lb = ('O=helpdesk.htm&usr=admin&pws=' + hashlib.md5(cfg.hub['pass'].encode('utf-8')).hexdigest())
requests.post(cfg.hub['url'] + '/login.cgi', cookies=cfg.cookies, data=lb)

# get pi and current ts
pi = requests.get(cfg.hub['url'] + '/cgi/renewPi.js', cookies=cfg.cookies).text
ts = int(datetime.datetime.now().strftime('%s%f')[:-3])

# get cfg id for updating known devices list
n = requests.get(cfg.hub['url'] + '/cgi/cgi_myNetwork.js?ts=' + str(ts), cookies=cfg.cookies).text
for line in n.splitlines():
    if re.search('known_devices_update', line):
        cfg_id = line.split(',')[1]

# generate the delete string
ds = ('CMD=&GO=my_network.htm&SET0='+ cfg_id + '%3Dd%252C' + mac + '%253B' + '&pi=' + pi)

# send delete request
dr = requests.post(cfg.hub['url'] + '/apply.cgi', data=(ds), cookies=cfg.cookies)
if (dr.status_code != 200):
    print ('ERROR: ', dr.status_code)
    print (dr.request.body)
    exit(1)
print('OK')
