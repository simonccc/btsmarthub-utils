#!/usr/bin/env python3 

import requests
# local config
import config as cfg

r = requests.post(cfg.hub['url'] + '/logout.cgi?GO=home.htm&usr=admin', cookies=cfg.cookies, allow_redirects=False)
