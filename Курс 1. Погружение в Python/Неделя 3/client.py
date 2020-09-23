# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 13:07:14 2020

@author: Govor_000
"""

import socket
import time
import re

class ClientError(Exception):
   """Класс исключений клиента"""
   pass

class Client(object):
    """Client class"""
    
    def __init__(self, host, port, timeout=None):
        try:
            self._sock = socket.create_connection((host, port),timeout)
        except socket.error as err:
            raise ClientError("Cannot create connection", err)
    
    def _read(self):
        data = b""

        while not data.endswith(b"\n\n"):
            try:
                data += self._sock.recv(1024)
            except socket.error as err:
                raise ClientError("Error reading data from socket", err)
                
        return data.decode('utf-8')

    def _send(self, data):

        try:
            self._sock.sendall(data)
        except socket.error as err:
            raise ClientError("Error sending data to server", err)
            
    
    def put(self, metric, value, timestamp=None):
        
        timestamp = timestamp or int(time.time())
        
        self._send(f'put {metric} {value} {timestamp}\n'.encode("utf8"))
        raw_data = self._read()
        if raw_data !='ok\n\n':
            raise ClientError('Server returns an error')      
            
    
    def get(self, metric):
        
        self._send(f'get {metric}\n'.encode("utf8"))
        raw_data = self._read()
        
        # Придется преобразовать ответ сервера к raw string
        recv_pattern = r'ok\\n(\w+(\.\w+)? \d+(\.\d+)? \d+\\n)*\\n'
        match = re.fullmatch(recv_pattern,("%r"%raw_data)[1:-1]) 
        if match:
            return Client.data_to_dict(raw_data)
        raise ClientError('Server returns an error or an invalid data') 
    
    def close(self):
        try:
            self._sock.close()
        except socket.error as err:
            raise ClientError("Error. Do not close the connection", err)
    
    @staticmethod
    def data_to_dict(raw_data):
        data_dict = {}
        splitted_data = raw_data.split()
        status, payload = splitted_data[0], splitted_data[1:]
        
        if status != 'ok':
            raise ClientError('Server returns an error')
            
        for i,key in enumerate(payload[0::3]):
            value, timestamp = payload[3*i+1], payload[3*i+2]
            data_dict[key] = data_dict.setdefault(key,[]) + [(int(timestamp), float(value))]
            data_dict[key].sort(key = lambda x: x[0])
        return data_dict

            
        
            
"""    

    @staticmethod
    def data_to_dict(raw_data):
        data_dict = {}
        status, payload = raw_data.split("\n", 1)
        for i,key in enumerate(payload[0::3]):
            value, timestamp = payload[3*i+1], payload[3*i+2]
            data_dict[key] = data_dict.setdefault(key,[]) + [(int(timestamp), float(value))]
            data_dict[key].sort(key = lambda x: x[0])
        return data_dict

        
client = Client("127.0.0.1", 8888, timeout=15)

client.put("palm.cpu", 0.5, timestamp=1150864247)
client.put("palm.cpu", 2.0, timestamp=1150864248)
client.put("palm.cpu", 0.5, timestamp=1150864248)

client.put("eardrum.cpu", 3, timestamp=1150864250)
client.put("eardrum.cpu", 4, timestamp=1150864251)
client.put("eardrum.memory", 4200000)

print(client.get("palm.cpu"))
print(client.get("*"))         
   
"""         
