#!/usr/bin/env python

#czyli Gracz 1 xD
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
   


# # a Python object (dict):
# x = {"board": []}
# cell = {"cell_0_0": {}}
# tile = {"empty": False, "color": "blue", "number": 3}
# cell["cell_0_0"] = tile

# cell1 = {"cell_0_1": {}}
# tile = {"empty": False, "color": "blue", "number": 1}
# cell1["cell_0_1"] = tile

# # cell["cell_0_0"] = tile
# x["board"].append(cell)
# x["board"].append(cell1)
# # convert into JSON:
# y = json.dumps(x)

f = open('GameBoard.json')
  
# returns JSON object as 
# a dictionary
data = str(json.load(f))
print(data)
Tcp_connect('192.168.56.1', 17098)
Tcp_Write(data)
print(Tcp_Read())
Tcp_Write('server')
print(Tcp_Read())
Tcp_Close()