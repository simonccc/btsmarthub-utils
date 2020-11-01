#!/usr/bin/env bash
while :;
do
./snmp-poller.py > smarthub.db
echo polled
sleep 10
done
