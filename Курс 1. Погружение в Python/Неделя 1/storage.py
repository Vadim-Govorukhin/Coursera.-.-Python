# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 14:53:03 2020

@author: Govor_000
"""

import os
import tempfile
import argparse
import json

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
#storage_path = os.path.join('C:/Stepik/Coursera. Специализация. Программирование на Python/Курс 1. Погружение в Python/Неделя 1/',
#                            'storage.data')
parser = argparse.ArgumentParser()
parser.add_argument("--key", help="Key")
parser.add_argument("--value", help="Value")
args = parser.parse_args()

key, value = args.key, args.value

if not os.path.exists(storage_path):
    open(storage_path, "w").close()

if key and value:
    with open(storage_path, 'r') as f:
        json_data = f.readline()
        if json_data:
            data_dict = json.loads(json_data)       
        else:
            data_dict = dict()            
        data_dict[key] = data_dict.get(key, []) + [value]
        json_data = json.dumps(data_dict)
        
    with open(storage_path, 'w') as f:
        f.write(json_data)
    
elif key:
    with open(storage_path, 'r') as f:
        json_data = f.readline()
        if json_data:
            data_dict = json.loads(json_data)
        else:
            data_dict = dict()
        print(*data_dict.get(key, []), sep=', ')   
else:
    print('The program is called with invalid parameters.')

#"""