DATA = {
   # sysDesc
   '1.3.6.1.2.1.1.1.0': lambda oid: octet_string((re.match('1.3.6.1.2.1.1.1.0:.*',(open('smarthub.db').read())).group()).split(':')[1]),
  # sets it as switchos
#  '1.3.6.1.2.1.1.2.0': object_identifier('.1.3.6.1.4.1.14988.2'),

  # uptime?
  '1.3.6.1.2.1.1.3.0': lambda oid: timeticks(int(uptime() * 100)),

  '1.3.6.1.2.1.1.4.0': octet_string(''),
  '1.3.6.1.2.1.1.5.0': octet_string('btsmarthub-snmpd-hack'),
  '1.3.6.1.2.1.1.6.0': octet_string(''),

  # interface count
  '1.3.6.1.2.1.2.1.0': integer(1),

  # interface 1
  '1.3.6.1.2.1.2.2.1.1.1': integer(1),
  '1.3.6.1.2.1.2.2.1.2.1': octet_string('test adapter'),
  # ethernet
  '1.3.6.1.2.1.2.2.1.3.1': integer(6),
  # mtu
  '1.3.6.1.2.1.2.2.1.4.1': integer(1500),
  # speed
  '1.3.6.1.2.1.2.2.1.5.1': gauge32(100000000),

  # mac address??
#  '1.3.6.1.2.1.2.2.1.6.1': octet_string('c4:ad:34:f7:7a:c0'),

# status = up
  '1.3.6.1.2.1.2.2.1.7.1': integer(1),
  '1.3.6.1.2.1.2.2.1.8.1': integer(1),

  # interface uptime
  '1.3.6.1.2.1.2.2.1.9.1': lambda oid: timeticks(int(uptime() * 100)),
# inoct
  '1.3.6.1.2.1.2.2.1.10.1': counter32(99122131),

# ??
  '1.3.6.1.2.1.2.2.1.11.1': counter32(99122131),
  '1.3.6.1.2.1.2.2.1.12.1': counter32(99123131),
  '1.3.6.1.2.1.2.2.1.13.1': counter32(3131),
  '1.3.6.1.2.1.2.2.1.14.1': counter32(0),
  '1.3.6.1.2.1.2.2.1.15.1': counter32(0),
# outoct
  '1.3.6.1.2.1.2.2.1.16.1': counter32(342545234),

# ??
  '1.3.6.1.2.1.2.2.1.17.1': counter32(738783728),
  '1.3.6.1.2.1.2.2.1.18.1': counter32(7878787),
  '1.3.6.1.2.1.2.2.1.19.1': counter32(0),
  '1.3.6.1.2.1.2.2.1.20.1': counter32(0),
  '1.3.6.1.2.1.2.2.1.21.1': gauge32(0),
}
