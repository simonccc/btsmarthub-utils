#!/usr/bin/env bash
while :;
do
./snmp-poller.py
echo -n "polled "
date
sleep 10
done
