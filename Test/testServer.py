#!/usr/bin/env python
import socket, time
import json

#things to begin with
def Tcp_connect( HostIp, Port ):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HostIp, Port))
    return
    
def Tcp_server_wait ( numofclientwait, port ):
	global s2
	s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s2.bind(('',port)) 
	s2.listen(numofclientwait) 

def Tcp_server_next ( ):
		global s
		s = s2.accept()[0]
   
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

	b_dict = eval(b) # dictionary format
	return b_dict

def Tcp_Close( ):
   s.close()
   return 


Tcp_server_wait ( 5, 17098 )
Tcp_server_next()
f = open('GameBoard.json')
# returns JSON object as 
# a dictionary
data = str(json.load(f))
#print(data)


while True:
	Tcp_Write(data)
	print(str(Tcp_Read()))
	print("----------------------------------------------")
	print()

	# Tcp_Write('hello')
	
Tcp_Close()
