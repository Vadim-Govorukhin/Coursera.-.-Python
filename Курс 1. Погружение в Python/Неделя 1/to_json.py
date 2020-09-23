# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 11:54:06 2020

@author: Govor_000
"""

import json
from functools import wraps

def to_json(func):
    
    @wraps(func)
    def inner(*args, **kwargs):
        return json.dumps(func(*args, **kwargs))
    
    return inner

"""
@to_json
def get_data():
  return {
    'data': 42
  }
  
get_data()  # вернёт '{"data": 42}'
#"""