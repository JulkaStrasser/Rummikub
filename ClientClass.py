#!/usr/bin/env python

#czyli Gracz 1 xD
import socket, time
import json


class Client:
    def __init__(self,host_ip, port,main):
        self.host_ip = host_ip
        self.port = port
        self.tileCollection = main.tileCollection

    def read_json_file(self,file_name):
        f = open(file_name)
        # returns JSON object as 
        # a dictionary
        data = str(json.load(f))
        #print(data)
        return data

    def Tcp_connect(self):
        self.s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
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
        self.b_dict = eval(b) # dictionary format
        
        self.JsonToGrid()
        self.b_dict

    def JsonToGrid(self):
        self.grid = []
        self.grid.clear()
        #print(str(self.b_dict['board']))
        for item in self.b_dict['board']:
            #print(item)

            # dostep do nazwy cell
            cell_name = str(list(item.keys())[0])
            #print(cell_name)
            is_cell_empty = item[cell_name]['empty']
            #print(is_cell_empty)
            if is_cell_empty == True:
                self.grid.append(None)
            else:
                color = item[cell_name]['color']
                number = item[cell_name]['number']
                tile_index = self.tileCollection.getTileColorNumber(color,number)
                self.grid.append(tile_index)
            
            print(self.grid)
            
            

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