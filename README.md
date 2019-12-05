# vigor2130-scrape-api
Scrape API Calls for the Draytek Vigor 2130 Router

/cgi-bin/webstax/stat/grocx_dhcp_status returns

A pipe separated string with forward separated records that contain the
computer name, ip address, mac address and dhcp expiry time in minutes. 
Note that there are no line endings in the returned string.

```
|*/192.168.1.239/33:44:55:66:77:88/189
|My-iPhone/192.168.1.241/11:22:33:44:55:66/216
|Chromecast/192.168.1.240/22:33:44:55:66:77/233|
```

/cgi-bin/webstax/config/arp_table returns

A newline separated string with tab separated records that contain the
ip address and mac address.
Note that there is a header at the beginning of the returned string. 

```
IP Address\t   MAC Address	\n
192.168.1.249\t11:22:33:44:55:66\n
10.138.0.1\t22:33:44:55:66:77\n
192.168.1.240\t33:44:55:66:77:88\n
```

/cgi-bin/webstax/stat/session returns

A newline separated string with space separated records that contain the 
protocol, source ip address and port, destination ip address and port and the 
connection state if the protocol is tcp.

```
tcp 192.168.1.243:50555 1.2.3.4:80 ESTABLISHED\n
udp 192.168.1.251:57655 2.3.4.5:2013\n
tcp 192.168.1.241:50512 3.4.5.6:22 TIME_WAIT\n
tcp 192.168.1.239:50463 4.5.6.7:53 CLOSE_WAIT\n
```

/cgi-bin/webstax/config/ipbmac returns

A forward slash separated string with three sections from which the third is returned from a pipe separated string with
comma separated values holding the ip address, mac address and computer name. Note that there are spare pipes at the end
of the section.

```
1/192.168.1.249\n
192.168.1.240,11:22:33:44:55:66\n
22:33:44:55:66:77\n
33:44:55:66:77:88/192.168.1.249,11:22:33:44:55:66,My-iPhone,0|192.168.1.240,22:33:44:55:66:77,Chromecast,0|
```
