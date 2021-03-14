# smarthub snmp support 

abandoned snmpd hack for the smarthub 

uses the snmpd server from https://github.com/delimitry/snmp-server

# howto

add the devices you want to poll in your config.py

each device needs a number 

run ./gen-config.py which generates smarthub-config.py

run poll.sh to run the snmp poller

then sudo ./snmp-server.py -c smarthub-config.py

( this does not work as further work would be required to calculate the correct values for octets - whilst it "works" and the data levels displayed in eg observium are representitive - they're wrong of course ) 
