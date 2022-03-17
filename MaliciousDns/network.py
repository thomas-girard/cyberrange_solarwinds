import os
import socket

string = "i32hu6i32hu6.appsync-api.us-east-2.avsvmcloud.com"


ban_ip = [
    "10.0.0.0",
    "172.16.0.0",
    "192.168.0.0",
    "224.0.0.0",
    "20.140.0.0",
    "96.31.172.0",
    "131.228.12.0",
    "144.86.226.0",
    "fc00:: - fe00::",
    "fec0:: - ffc0::",
    ]

ban_ip_range = [["fc00", ]]

ip_list = []
ais = socket.getaddrinfo("www.google.com",0,0,0,0)
for result in ais:
  ip_list.append(result[-1][0])
ip_list = list(set(ip_list))

