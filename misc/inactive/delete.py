#!/usr/bin/env python3 

import datetime, re, requests, hashlib, sys
sys.path[0:0] = ['../../']
import config as cfg

login_body = ('O=helpdesk.htm&usr=admin&pws=' + hashlib.md5(cfg.hub['pass'].encode('utf-8')).hexdigest())
login = requests.post(cfg.hub['url'] + '/login.cgi', cookies=cfg.cookies, data=login_body)
pi = requests.get(cfg.hub['url'] + '/cgi/renewPi.js', cookies=cfg.cookies).text
ts = int(datetime.datetime.now().strftime('%s%f')[:-3])
n = requests.get(cfg.hub['url'] + '/cgi/cgi_myNetwork.js?ts=' + str(ts)).text
for line in n.splitlines():
    if re.search('known_devices_update', line):
        cfg_id = line.split(',')[1]

delstring = ('CMD=&GO=my_network.htm&SET0='+ cfg_id + '%3Dd%252C' + sys.argv[1] + '%253B' + '&pi=' + pi)
header = {'Origin': cfg.hub['url']}
delete = requests.post(cfg.hub['url'] + '/apply.cgi', data=(delstring), cookies=cfg.cookies, headers=header)
print(delete.request.headers)
print(delete.request.body)
print (delete.status_code)
#go = requests.get(cfg.hub['url'] + '/my_network.htm', cookies=cfg.cookies)
#print (go.status_code)


