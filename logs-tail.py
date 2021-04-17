#!/usr/bin/env python3

import requests, time, datetime, urllib.parse, hashlib, signal, sys, math, re

# local config
import config as cfg

# year hack
year = (' ' + str((datetime.datetime.now()).year))

# body of login request
login_body = ('O=helpdesk.htm&usr=admin&pws=' + hashlib.md5(cfg.hub['pass'].encode('utf-8')).hexdigest())

# max amount of events to check
max_event_count=50

# login to router
def login():
#  print('logging in...')
  login = requests.post(cfg.hub['url'] + '/login.cgi', cookies=cfg.cookies, data=login_body, allow_redirects=False)
  time.sleep(1)

def print_c(color, string):
  if cfg.tail_colors['enabled'] == 'true':
   return(cfg.tail_colors[color] + string  + '\x1b[0m ')
  else:
   return(string)

def timestamp_short(timestamp):
  return(datetime.datetime.fromtimestamp(int(timestamp)).strftime('%H:%M:%S'))

def signal_handler(signal, frame):
  sys.exit(0)

# get the current ts - 10 seconds
ts = int(time.time()) - 10
short_start_time = timestamp_short(ts)
print(print_c('green', (str(short_start_time)) + " start up"))

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
  r = requests.get(cfg.hub['url'] + '/cgi/cgi_helpdesk.js?t=' + str(ts), cookies=cfg.cookies, allow_redirects=False)

  # if a 302 login
  if (str(r.status_code) == '302'):
    login()
    continue

  else:
    # split by var
    vars = r.content.decode().split(";")

    # search for the event log var
    for var in vars:
      if re.search('evtlog', var):
        # split log by ,
        events = (var.split(","))
      else:
        continue

    for event in events:

        # first ( latest ) event needs cleaning up
        if event_count == 0:
           event  = event.replace("var evtlog_list=[", "").strip('\r\n')

        # decode the content
        url_decoded = urllib.parse.unquote(event)

        # remove extra characters
        event = url_decoded.replace("['","").replace("']","").strip('\n')

        # split the event by time and event
        event_split = event.split(". ")

        # add the in year
        log_time = (event_split[0] + year)
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

        # print log entry
        print((print_c('blue',sts) + print_c('yellow',prog) + prog_event))

        # set ts to the latest log tss
        ts = event_timestamp

    # assume we have processed all the events for this second and increment it
    if ( str(ts) == str(event_timestamp)):
        ts = (int(ts) + 1 )

  # sleep
  time.sleep(10)
