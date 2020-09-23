# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 14:44:59 2020

@author: Govor_000
"""

import mypackage.utils

# print(mypackage)

"""
Каждый модуль содержит в своем пространстве имен
переменную __name__, которая определяет название модуля, 
в котором выполняется код. Это позволяет разделить
те моменты, когда наш модуль используется напрямую
интерпретатором Python, либо он был импортирован из другого модуля.
"""
if __name__ == "__main__": 
   # print("hello")
   print(mypackage.utils.multiply(2,6))
   
import this
import inspect

# Где находится файл
print(inspect.getfile(this))