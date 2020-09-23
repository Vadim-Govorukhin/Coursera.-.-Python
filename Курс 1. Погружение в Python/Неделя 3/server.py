# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 15:23:32 2020

@author: Govor_000
"""


import asyncio
from collections import defaultdict

    
class ClientServerProtocol(asyncio.Protocol):
    
    _data = defaultdict(dict)
    """
    # настройки сообщений сервера
    sep = '\n'
    error_message = "wrong command"
    code_err = 'error'
    code_ok = 'ok'
    """
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print('--'*10)
        print('Запрос',data)
        resp = self.process_data(data.decode())
        print('Ответ',resp.encode())
        # отправляем ответ
        self.transport.write(resp.encode())
        
    def process_data(self, data):  
        """Метод data_received вызывается при получении данных в сокете"""
        
        splitted_data = data.split()
        try:
            command, payload = splitted_data[0], splitted_data[1:]
        except IndexError:
            return 'error\nwrong command\n\n'
        
        if   command == 'put' and len(payload) % 3 == 0:
            return self.put_data(payload)
        elif command == 'get' and len(payload) == 1:
            return self.get_data(payload[0])
        else:
            return 'error\nwrong command\n\n'
        
    def put_data(self, payload):
        # Проверим данные на валидность
        try:
            list(map(float,payload[1::3]))
            list(map(int  ,payload[2::3]))
        except ValueError:
            return 'error\nwrong command\n\n' 
        for i,key in enumerate(payload[0::3]):
            value, timestamp = payload[3*i+1], payload[3*i+2]
            self._data[key][int(timestamp)] = float(value)

            
        return 'ok\n\n'
    
        
    def get_data(self, metric):
        if metric =='*':
            return ClientServerProtocol.dict_to_data(self._data)
        elif metric in self._data.keys():
            return ClientServerProtocol.dict_to_data({metric: self._data[metric]})
        else:
            return 'ok\n\n'
        
              
    @staticmethod
    def dict_to_data(dic):
        resp = 'ok\n'
        for key, values in dic.items():
            for timestamp, value in values.items():
                resp += f'{key} {value} {timestamp}\n'
        resp += '\n'
        return resp

def run_server(host, port):
    loop = asyncio.get_event_loop()
    coroutine = loop.create_server(
        ClientServerProtocol,
        host, port
    )
    
    server = loop.run_until_complete(coroutine)
    
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == "__main__":
    run_server("127.0.0.1", 8888)
    
