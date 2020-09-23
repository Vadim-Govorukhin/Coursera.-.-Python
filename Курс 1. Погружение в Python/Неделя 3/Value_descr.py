# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 13:27:16 2020

@author: Govor_000
"""

class Value:
    
    def __init__(self):
        self.value = None
        
    @staticmethod
    def _prepare_value(value, commission):
        return value*(1 - commission)
    
    def __get__(self, obj, obj_type):
        return self.value
    
    def __set__(self, obj, value):
        self.value = self._prepare_value(value, obj.commission)
        
    

"""
class Account:
    amount = Value()
    
    def __init__(self, commission):
        self.commission = commission
        
        
        
        
        
new_account = Account(0.2)
new_account.amount = 1000

print(new_account.amount)
"""