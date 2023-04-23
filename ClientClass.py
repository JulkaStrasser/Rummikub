#!/usr/bin/env python

#czyli Gracz 1 xD
import socket, time
import json

class Client:
    def __init__(self,host_ip, port):
        self.host_ip = host_ip
        self.port = port

    def read_json_file(self,file_name):
        f = open(file_name)
        # returns JSON object as 
        # a dictionary
        data = str(json.load(f))
        #print(data)
        return data

    def Tcp_connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host_ip, self.port))
        return
    
    def Tcp_Write(self,D):
        mes = str(D + '\r')
        self.s.send(mes.encode())
        return 
        
    def Tcp_Read(self):
        a = ' '
        b = ''
        while a != '\r':
            a = self.s.recv(1).decode()
            b = b + a
        b_dict = eval(b) # dictionary format
        return b_dict

    def Tcp_Close(self):
        self.s.close()
        return 
   
# client = Client('192.168.56.1', 17098)
# client.Tcp_connect()

# data = client.read_json_file('GameBoard.json')

# client.Tcp_Write(data)
# print(client.Tcp_Read())
# client.Tcp_Write('server')
# print(client.Tcp_Read())

# client.Tcp_Close()