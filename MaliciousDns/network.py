import os
import socket
import sys

domain_name = "i32hu6i32hu6.appsync-api.us-east-2.avsvmcloud.com" # = sortie de algo DGA

ban_ip = [
    "10.0.0.0",
    "172.16.0.0",
    "192.168.0.0",
    "224.0.0.0",
    "20.140.0.0",
    "96.31.172.0",
    "131.228.12.0",
    "144.86.226.0",
    ]

ban_ip_range = [["fc00", "fe00"], ["fec0", "ffc0"], ["ff00", "ff00"]]



def main():

  ip_list = []
  ais = socket.getaddrinfo(domain_name,0,0,0,0)
  for result in ais:
    ip_list.append(result[-1][0])
  ip_list = list(set(ip_list))

  print(ip_list)
  stop=False
  for ip in ip_list:
    if ":" not in ip:
      if ip in ban_ip:
        stop=True
        break
    else:
      for [min_ip, max_ip] in ban_ip_range:
        if ip[:4] >= min_ip and ip[:4] <= max_ip:
          stop=True
          break


  if stop == True:
    print("arrêt du malware, détection d'une IP bannie")




if __name__=="__main__":
  main()
  sys.exit(0)



