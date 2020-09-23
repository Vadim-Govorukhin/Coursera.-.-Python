# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 12:54:54 2020

@author: Govor_000
"""

class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""
        

class EventGet:
    
    def __init__(self, kind):
        self.kind = 'GET_' + str(kind).upper().split('\'')[1]
        self.prop = value;

        
class EventSet:
    
    def __init__(self, value):
        self.kind = 'SET_' + str(type(value)).upper().split('\'')[1]
        self.value = value
     
        
class NullHandler:
    
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)

class IntHandler(NullHandler):    
    
    def handle(self, obj, event):
        if event.kind == "GET_INT":
            return obj.integer_field        
        elif event.kind == "SET_INT":
            obj.integer_field = event.value
            print('here', obj.integer_field)
        else:
            print("Передаю обработку дальше")
            return super().handle(obj, event)


class FloatHandler(NullHandler):
    
    def handle(self, obj, event):
        
        if event.kind == "GET_FLOAT":
            return obj.float_field 
        elif event.kind == "SET_FLOAT":
            obj.float_field = event.value            
        else:
            print("Передаю обработку дальше")
            return super().handle(obj, event)


class StrHandler(NullHandler):
    
    def handle(self, obj, event):
        if event.kind == "GET_STR":
            return obj.string_field        
        elif event.kind == "SET_STR":
            obj.string_field = event.value
        else:
            print("Передаю обработку дальше")
            return super().handle(obj, event)
"""
obj = SomeObject()
obj.integer_field = 42
obj.float_field = 3.14
obj.string_field = "some text"

chain = IntHandler(FloatHandler(StrHandler(NullHandler())))

#print(chain.handle(obj, EventGet(int)))
# 42
#print(chain.handle(obj, EventGet(float)))
#3.14
#print(chain.handle(obj, EventGet(str)))
#'some text'
chain.handle(obj, EventSet(100))
print(chain.handle(obj, EventGet(int)))
#100
chain.handle(obj, EventSet(0.5))
print(chain.handle(obj, EventGet(float)))
#0.5
chain.handle(obj, EventSet('new text'))
print(chain.handle(obj, EventGet(str)))
#'new text'


"""













