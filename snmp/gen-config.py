#!/usr/bin/env python3 

import sys

# read config from root directory
sys.path[0:0] = ['../']
import config as cfg

config = open('smarthub-config.py', "w")
config.write('''DATA = {
# sysDesc
'1.3.6.1.2.1.1.1.0': lambda oid: octet_string((re.search(oid +'_.*',(open('smarthub.db').read())).group()).split('_')[1]),

# uptime
'1.3.6.1.2.1.1.3.0': lambda oid: timeticks(int((re.search(oid +'_.*',(open('smarthub.db').read())).group()).split('_')[1])),

# sets it as switchos
#'1.3.6.1.2.1.1.2.0': object_identifier('.1.3.6.1.4.1.14988.2'),

# contact
'1.3.6.1.2.1.1.4.0': octet_string(''),

# hostname
'1.3.6.1.2.1.1.5.0': octet_string('btsmarthub-snmpd-hack'),

# location
'1.3.6.1.2.1.1.6.0': octet_string('http://bthub.home/'),

# interface count
'1.3.6.1.2.1.2.1.0': lambda oid: integer(int((re.search(oid +'_.*',(open('smarthub.db').read())).group()).split('_')[1])),

''')

for int in cfg.snmp:
    name = (cfg.snmp[int][1])
    int_no = (cfg.snmp[int][0])

    # interface no
    config.write('\'1.3.6.1.2.1.2.2.1.1.' + int_no + '\': integer(' + int_no +'),\n')

    # interface name
    config.write('\'1.3.6.1.2.1.2.2.1.2.' + int_no + '''\': lambda oid: octet_string((re.search(oid +'_.*',(open('smarthub.db').read())).group()).split('_')[1]),\n''')

    # ethernet
    config.write('\'1.3.6.1.2.1.2.2.1.3.' + int_no + '''\': integer(6),\n''')

    # mtu
    config.write('\'1.3.6.1.2.1.2.2.1.4.' + int_no + '''\': integer(1500),\n''')

    # speed
    config.write('\'1.3.6.1.2.1.2.2.1.5.' + int_no + '''\': gauge32(1000000000),\n''')

      # mac address??
      #  '1.3.6.1.2.1.2.2.1.6.1': octet_string('c4:ad:34:f7:7a:c0'),

    # status
    config.write('\'1.3.6.1.2.1.2.2.1.7.' + int_no + '''\': integer(1),\n''')
    config.write('\'1.3.6.1.2.1.2.2.1.8.' + int_no + '''\': integer(1),\n''')

    # uptime
    config.write('\'1.3.6.1.2.1.2.2.1.9.' + int_no + '''\': lambda oid: timeticks(int((re.search(oid +'_.*',(open('smarthub.db').read())).group()).split('_')[1])), \n''')

    # inocts
    config.write('\'1.3.6.1.2.1.2.2.1.10.' + int_no + '''\': lambda oid: counter64(int((re.search(oid +'_.*',(open('smarthub.db').read())).group()).split('_')[1])), \n''')

    # outocts
    config.write('\'1.3.6.1.2.1.2.2.1.16.' + int_no + '''\': lambda oid: counter64(int((re.search(oid +'_.*',(open('smarthub.db').read())).group()).split('_')[1])), \n''')

    config.write('\n\n')

config.write('''}''')
config.close
