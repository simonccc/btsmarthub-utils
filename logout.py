#!/usr/bin/env python3 

import requests
import socket
import urllib.parse
import hashlib
# local config
import config as cfg

# generate a uniqe token for this host
md5 = hashlib.md5()
md5.update(str(socket.gethostname()).encode('utf-8'))
urn = md5.hexdigest()

cookies = {
'logout': 'yes',
'urn': urn
}

r = requests.post(cfg.hub['url'] + '/logout.cgi?GO=home.htm&usr=admin', cookies=cookies, allow_redirects=False)
