import socket

client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

client.connect(("localhost", 9999))

client.send("Hello From Client".encode())
print(client.recv(1024).decode())