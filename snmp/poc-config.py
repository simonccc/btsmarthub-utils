DATA = {

 # sysDesc
 '1.3.6.1.2.1.1.1.0': lambda oid: octet_string((re.search(oid +'_.*',(open('smarthub.db').read())).group()).split('_')[1]),

  # uptime
  '1.3.6.1.2.1.1.3.0': lambda oid: timeticks(int((re.search(oid +'_.*',(open('smarthub.db').read())).group()).split('_')[1])),

  # sets it as switchos
#  '1.3.6.1.2.1.1.2.0': object_identifier('.1.3.6.1.4.1.14988.2'),

  # contact
  '1.3.6.1.2.1.1.4.0': octet_string(''),

  # hostname
  '1.3.6.1.2.1.1.5.0': octet_string('btsmarthub-snmpd-hack'),

  # location
  '1.3.6.1.2.1.1.6.0': octet_string('http://bthub.home/'),

  # interface count
  '1.3.6.1.2.1.2.1.0': lambda oid: integer(int((re.search(oid +'_.*',(open('smarthub.db').read())).group()).split('_')[1])),

  # interface 1
  '1.3.6.1.2.1.2.2.1.1.1': integer(1),
  '1.3.6.1.2.1.2.2.1.2.1': lambda oid: octet_string((re.search(oid +'_.*',(open('smarthub.db').read())).group()).split('_')[1]),
  # ethernet
  '1.3.6.1.2.1.2.2.1.3.1': integer(6),
  # mtu
  '1.3.6.1.2.1.2.2.1.4.1': integer(1500),
  # speed
  '1.3.6.1.2.1.2.2.1.5.1': gauge32(1000000000),

  # mac address??
#  '1.3.6.1.2.1.2.2.1.6.1': octet_string('c4:ad:34:f7:7a:c0'),

# status = up
  '1.3.6.1.2.1.2.2.1.7.1': integer(1),
  '1.3.6.1.2.1.2.2.1.8.1': integer(1),

  # interface uptime
  '1.3.6.1.2.1.2.2.1.9.1': lambda oid: timeticks(int((re.search(oid +'_.*',(open('smarthub.db').read())).group()).split('_')[1])),

# inoct
  '1.3.6.1.2.1.2.2.1.10.1': lambda oid: counter32(int((re.search(oid +'_.*',(open('smarthub.db').read())).group()).split('_')[1])),
#  '1.3.6.1.2.1.2.2.1.10.1': counter32(99122131),

# ??
#  '1.3.6.1.2.1.2.2.1.11.1': counter32(0),
#  '1.3.6.1.2.1.2.2.1.12.1': counter32(0),
#  '1.3.6.1.2.1.2.2.1.13.1': counter32(0),
#  '1.3.6.1.2.1.2.2.1.14.1': counter32(0),
#  '1.3.6.1.2.1.2.2.1.15.1': counter32(0),
# outoct
  '1.3.6.1.2.1.2.2.1.16.1': lambda oid: counter32(int((re.search(oid +'_.*',(open('smarthub.db').read())).group()).split('_')[1])),

# ??
#  '1.3.6.1.2.1.2.2.1.17.1': counter32(0),
#  '1.3.6.1.2.1.2.2.1.18.1': counter32(0),
#  '1.3.6.1.2.1.2.2.1.19.1': counter32(0),
#  '1.3.6.1.2.1.2.2.1.20.1': counter32(0),
#  '1.3.6.1.2.1.2.2.1.21.1': gauge32(0),
}
