#!/usr/bin/env bash
while :;
do
./snmp-poller.py
echo -n "polled "
date
cat smarthub.db
sleep 10
done
