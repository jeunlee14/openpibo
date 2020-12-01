#!/bin/bash
sleep 20
EIP=$(ifconfig eth0 | grep "inet " | awk '{print $2}') || true
SSID=$(iw wlan0 info | grep ssid | awk '{print $2}') || true
WIP=$(ifconfig wlan0 | grep "inet " | awk '{print $2}') || true

if [ "$EIP" = "" ];then
  EIP="-"
fi
if [ "$SSID" = "" ];then
  SSID="-"
fi
if [ "$WIP" = "" ];then
  WIP="-"
fi

python3 /home/pi/openpibo/utils/boot/net_info.py --eip $EIP --wip $WIP --ssid $SSID
