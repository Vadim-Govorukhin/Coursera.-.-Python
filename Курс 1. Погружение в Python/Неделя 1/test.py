# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 15:48:27 2020

@author: Govor_000
"""

import json

data_json = json.dumps({"c": 0, "b": 0, "a": 0})
print(data_json)
data_dict = json.loads('{"c": 0, "b": 0, "a": 0}')
print(data_dict)