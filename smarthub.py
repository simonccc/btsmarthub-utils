import requests
import os
import time
import datetime
import urllib.parse
import hashlib
import sys

import logging
import logging.handlers

DOCKER_URL=os.environ['URL']
DOCKER_PASS=os.environ['PASS']
DOCKER_LOGHOST=os.environ['LOGHOST']
DOCKER_LOGHOST_PORT=os.environ['LOGHOST_PORT']
DOCKER_SMARTHUB_NAME=os.environ['SMARTHUB_NAME']

cookies = {
'logout': 'not',
'urn': 'kXX2kkkklk11x'
}

# setup sysloging
my_logger = logging.getLogger('smarthub')
my_logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = (DOCKER_LOGHOST,int(DOCKER_LOGHOST_PORT)))
my_logger.addHandler(handler)

# body of login request
login_body = ('O=helpdesk.htm&usr=admin&pws=' + hashlib.md5(DOCKER_PASS.encode('utf-8')).hexdigest())

# max amount of events to check
max_event_count=50

def login():
  login = requests.post(DOCKER_URL + '/login.cgi', cookies=cookies, data=login_body, allow_redirects=False)

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

      # if event timestamp is greater than the current 
      if ( ( str(event_timestamp) >= str(ts) ) and ( str((parsed_events[i])[1]) != str(event_data) )):

        # map event data
        event_data = str(((parsed_events[i])[1]))
        prog_data = event_data.split()
        prog = prog_data[0]
        prog_data.remove(prog)
        prog_event = ' '.join(prog_data)

        # syslog event
        syslog_event = (str(sts) + '.00000 ' + DOCKER_SMARTHUB_NAME + ' ' +  str(prog) + ': ' +  str(prog_event))
        print(syslog_event,file=sys.stderr)

        # print log entry
        my_logger.info(syslog_event)

        # set ts to the latest log tss
        ts = event_timestamp

    # assume we have processed all the events for this second and increment it
    if ( str(ts) == str(event_timestamp)):
        ts = (int(ts) + 1 )

  # sleep
  time.sleep(10)
