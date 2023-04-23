#!/usr/bin/env python
import socket, time
import json
def Tcp_connect( HostIp, Port ):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HostIp, Port))
    return
   
def Tcp_Write(D):
   mes = str(D + '\r')
   s.send(mes.encode())
   return 
   
def Tcp_Read( ):
	a = ' '
	b = ''
	while a != '\r':
		a = s.recv(1).decode()
		b = b + a
	return b

def Tcp_Close( ):
   s.close()
   return 
   
jsonResult = {"first":"You're", "second":"Awsome!"}
jsonResult = json.dumps(jsonResult)

Tcp_connect('192.168.56.1', 17098)
Tcp_Write(jsonResult)
print(Tcp_Read())
Tcp_Write('server')
print(Tcp_Read())
Tcp_Close()