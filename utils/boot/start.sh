#!/bin/bash
E0=$(ifconfig eth0 2>/dev/null | grep "inet " | awk '{print $2}') || true
E1=$(ifconfig eth1 2>/dev/null| grep "inet " | awk '{print $2}') || true
W0=$(ifconfig wlan0 2>/dev/null| grep "inet " | awk '{print $2}') || true
if [ "$W0" = "" ];then
  S0=""	
else
  S0=$(iw wlan0 info | grep ssid | awk '{print $2}') || true
fi
W1=$(ifconfig wlan1 2>/dev/null| grep "inet " | awk '{print $2}') || true
if [ "$W1" = "" ];then
  S1=""	
else
  S1=$(iw wlan0 info | grep ssid | awk '{print $2}') || true
fi

python3 /home/pi/openpibo/utils/boot/net_info.py --eip "$E0,$E1" --wip "$W0,$S0,$W1,$S1" 
