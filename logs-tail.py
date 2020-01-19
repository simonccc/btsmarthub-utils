#!/usr/bin/env python3 

import requests
import random
import time
import datetime
import socket
import urllib.parse
import hashlib
import signal
import sys
import math
# local config
import config as cfg

# generate a uniqe token for this host
md5 = hashlib.md5()
md5.update(str(socket.gethostname()).encode('utf-8'))
urn = md5.hexdigest()

# generate the hash of password used to login
md5 = hashlib.md5()
md5.update(cfg.hub['pass'].encode())
passw=md5.hexdigest()

# body of login request
login_body = ('O=helpdesk.htm&usr=admin&pws=' + passw)

# max amount of events to check
max_event_count=50

cookies = {
'logout': 'not',
'urn': urn
}

def login():
  login = requests.post(cfg.hub['url'] + '/login.cgi', cookies=cookies, data=login_body, allow_redirects=False)

def timestamp_short(timestamp):
  return(datetime.datetime.fromtimestamp(int(timestamp)).strftime('%H:%M:%S'))

def signal_handler(signal, frame):
  sys.exit(0)

# get the current ts - 10 seconds
ts = int(time.time()) - 10
short_start_time = timestamp_short(ts)
print('starting at: ' + str(short_start_time))

# Ctrl+C handler
signal.signal(signal.SIGINT, signal_handler)

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
  r = requests.get(cfg.hub['url'] + '/cgi/cgi_helpdesk.js?t=' + str(ts), cookies=cookies, allow_redirects=False)

  # if a 302 login
  if (str(r.status_code) == '302'):
    login()
    continue

  else:
    content = r.content
    vars = content.decode().split(";")

    #fw_update_time = urllib.parse.unquote((vars[6].split("="))[1])
    #print('fw_update_time', fw_update_time)

    # split the event log var 
    events = (vars[34].split(","))

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

#      print ('i:' + i + ' ts: ' + str(ts) + ' event timestamp: ' + str(event_timestamp))
#      print('eventdata: ' + event_data)
#      print('log eventdata: ' + str(((parsed_events[i])[1])))

      # if event timestamp is greater than the current 
      if ( ( str(event_timestamp) >= str(ts) ) and ( str((parsed_events[i])[1]) != str(event_data) )):

        # map event data
        event_data = str(((parsed_events[i])[1]))

        # print log entry
        print(sts + " " + event_data)

        # set ts to the latest log tss
        ts = event_timestamp

    # assume we have processed all the events for this second and increment it
    if ( str(ts) == str(event_timestamp)):
        ts = (int(ts) + 1 )

  # sleep
  time.sleep(5)
