import socket

HOST = '192.168.43.198'
PORT = 8081 # 2222
server = socket.socket()
server.bind((HOST, PORT))
print('[+] Serveur démarré')
print('[+] Attente d\'une connection client ...')
server.listen(1)
client, client_addr = server.accept()
print(f'[+] {client_addr} Client connecté au serveur')

while True:
    command = input('Entrez une commande : ')
    command = command.encode()
    client.send(command)
    print('[+] Commande envoyée')
    output = client.recv(1024)
    output = output.decode()
    print(f"Output: {output}")