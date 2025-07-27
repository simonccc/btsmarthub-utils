#!/usr/bin/env python3

import requests
import urllib.parse
import hashlib
import sys

sys.path[0:0] = ['../']
import config as cfg

MAX_STATS = 21

def print_c(color, string):
    """Return a colored string if enabled in config."""
    if cfg.tail_colors['enabled'] == 'true':
        return cfg.tail_colors[color] + string + '\x1b[0m '
    else:
        return string

def login():
    """Login to the hub as admin."""
    print(print_c('red', 'logging in...'))
    login_body = (
        'O=helpdesk.htm&usr=admin&pws=' +
        hashlib.md5(cfg.hub['pass'].encode('utf-8')).hexdigest()
    )
    requests.post(cfg.hub['url'] + '/login.cgi', cookies=cfg.cookies, data=login_body, allow_redirects=False)

def fetch_status():
    """Fetch the status page, logging in if needed."""
    r = requests.get(cfg.hub['url'] + '/cgi/cgi_helpdesk.js', cookies=cfg.cookies, allow_redirects=False)
    if str(r.status_code) == '302':
        login()
        r = requests.get(cfg.hub['url'] + '/cgi/cgi_helpdesk.js', cookies=cfg.cookies, allow_redirects=False)
    return r.content

def main():
    """Main logic to parse and print hub status vars."""
    content = fetch_status()
    vars_ = content.decode().split(";")
    count = 0

    for var in vars_:
        var_o = var.strip('\r\n')
        var_list = var_o.split(",")
        try:
            if var_list[1]:
                continue
        except IndexError:
            stats = var_list[0].split("=")
            if len(stats) < 2 or not stats[1]:
                continue
            print(print_c('green', stats[0]), print_c('yellow', urllib.parse.unquote(stats[1])))
            count += 1
            if count > MAX_STATS:
                break

if __name__ == "__main__":
    main()
