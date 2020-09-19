import requests
import os
import re
import time
import datetime
import urllib.parse
import hashlib
import sys

import graphyte

import logging
import logging.handlers

import random
import string

DEBUG = None
DOCKER_URL = None
DOCKER_PASS = None
DOCKER_LOGHOST = None
DOCKER_LOGHOST_PORT = None
DOCKER_SMARTHUB_NAME = None
DOCKER_G_HOST = None
DOCKER_G_PREFIX = None

try:
  DEBUG=os.environ['DEBUG']
except:
  pass

# login details
try:
  DOCKER_URL=os.environ['URL']
  DOCKER_PASS=os.environ['PASS']
except:
  print('NO URL OR PASS DEFINED. EXITING',file=sys.stderr)
  sys.exit(1)

# syslog
try:
  DOCKER_LOGHOST=os.environ['LOGHOST']
  DOCKER_LOGHOST_PORT=os.environ['LOGHOST_PORT']
  DOCKER_SMARTHUB_NAME=os.environ['SMARTHUB_NAME']
except:
  pass

# graphite
try:
  DOCKER_G_HOST=os.environ['G_HOST']
  DOCKER_G_PREFIX=os.environ['G_PREFIX']
except:
  pass

# used in default messages so needs to be set 
if DOCKER_SMARTHUB_NAME is None:
  DOCKER_SMARTHUB_NAME = 'smarthub'

urn = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 12)) 

print('URN: ', urn)

# cookies used for logging in
cookies = {
'logout': 'not',
'urn': urn
}

# activate syslog
if DOCKER_LOGHOST is not None:

  # use default syslog port if not passed
  if DOCKER_LOGHOST_PORT is None:
    DOCKER_LOGHOST_PORT = '512'

  print('SYSLOGGING AS: ' + DOCKER_SMARTHUB_NAME + " TO: " +  DOCKER_LOGHOST + ':' + DOCKER_LOGHOST_PORT, file=sys.stderr)

  my_logger = logging.getLogger('smarthub')
  my_logger.setLevel(logging.DEBUG)
  handler = logging.handlers.SysLogHandler(address = (DOCKER_LOGHOST,int(DOCKER_LOGHOST_PORT)))
  my_logger.addHandler(handler)

else:
  print('NO SYSLOG ACTIVATED',file=sys.stderr)

# activate graphite
if DOCKER_G_HOST is not None:
  if DOCKER_G_PREFIX is None:
    DOCKER_G_PREFIX = 'smarthub'
  print('SENDING BW METRICS TO: ' + DOCKER_G_HOST + ' prefix:' + DOCKER_G_PREFIX,file=sys.stderr)
  graphyte.init(DOCKER_G_HOST, prefix=DOCKER_G_PREFIX, interval=20)
else:
  print('NO GRAPHITEACTIVATED',file=sys.stderr)

# body of login request
login_body = ('O=helpdesk.htm&usr=admin&pws=' + hashlib.md5(DOCKER_PASS.encode('utf-8')).hexdigest())

# max amount of events to check
max_event_count=50

# login function
def login():
  login_ts = int(time.time())
  print('LOGGING IN AT: ' + str(login_ts) + " " + login_body, file=sys.stderr)
  login = requests.post(DOCKER_URL + '/login.cgi', cookies=cookies, data=login_body, allow_redirects=False)
  time.sleep(2)

def timestamp_short(timestamp):
  return(datetime.datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%dT%H:%M:%S"))

# get the current ts - 10 seconds
ts = int(time.time()) - 10
short_start_time = timestamp_short(ts)

# define event_data and timestamp
event_data = ""
event_timestamp = ""

# main loop
while True:

  # reset the event count
  event_count=int(0)

  # reset the event dict
  parsed_events = {}

  # request status page with latest time stamp
  r = requests.get(DOCKER_URL + '/cgi/cgi_helpdesk.js?t=' + str(ts), cookies=cookies, allow_redirects=False)

  # if a 302 login
  if (str(r.status_code) == '302'):
    login()
    continue

  else:
    content = r.content
    vars = content.decode().split(";")

    # split the event log var
    events = (vars[32].split(","))

    for event in events:

        # first ( latest ) event needs cleaning up
        if  event_count == 0:
            event  = event.replace("var evtlog_list=[", "").strip('\r\n')

        # decode the content
        url_decoded = urllib.parse.unquote(event)

        # remove extra characters
        event = url_decoded.replace("['","").replace("']","").strip('\n')

        # split the event by time and event
        event_split = event.split(". ")

        # add the in year ( fix me )
        log_time = (event_split[0] + ' 2020')
        log_event = (event_split[1])

        # convert the log date to timestamp
        log_ts = int(time.mktime(datetime.datetime.strptime(log_time, "%H:%M:%S, %d %b %Y").timetuple()))

        # add the event the parsed events dict
        parsed_events.update( { str(event_count): ( str(log_ts), str(log_event) )  } )

        # increment event count
        event_count += 1

        # we have reached the max event count so stop processing
        if event_count == int(max_event_count):
           break

    # get results  in reverse order
    for i in sorted(parsed_events, key=int, reverse=True):

      event_timestamp = (parsed_events[i])[0]
      sts = timestamp_short(event_timestamp)

      # if event timestamp is greater than the current
      if ( ( str(event_timestamp) >= str(ts) ) and ( str((parsed_events[i])[1]) != str(event_data) )):

        # map event data
        event_data = str(((parsed_events[i])[1]))

        # syslog event
        syslog_event = (str(sts) + '.00000 ' + DOCKER_SMARTHUB_NAME + ' syslog: ' + str(event_data))
        if DEBUG is not None:
          print('LOG: ' + syslog_event,file=sys.stderr)

        if DOCKER_LOGHOST is not None:
          my_logger.info(syslog_event)

        # set ts to the latest log tss
        ts = event_timestamp

    # assume we have processed all the events for this second and increment it
    if ( str(ts) == str(event_timestamp)):
        ts = (int(ts) + 1 )

  vars = (requests.get(DOCKER_URL + '/cgi/cgi_basicMyDevice.js').content.decode()).split('var')
  rate = vars[2].split('\n')

  for rate in rate:
    rate = urllib.parse.unquote(rate.replace('\'', ''))
    rate_items = rate.split(',')
    if ( re.search('timestamp', rate_items[0])):
       rate_mac = (rate_items[2].replace('mac:', '')).upper()
       tx = (rate_items[3].replace('tx:', ''))
       rx = (rate_items[4].replace('rx:', ''))
       rx = rx.replace('}','')

       if DEBUG is not None:
         print('METRICS: ',rate_mac + '.' + 'tx',tx)
         print('METRICS: ',rate_mac + '.' + 'rx',rx)

       if DOCKER_G_HOST is not None:
         graphyte.send(rate_mac + '.' + 'tx',int(tx))
         graphyte.send(rate_mac + '.' + 'rx',int(rx))

  # sleep
  time.sleep(30)
