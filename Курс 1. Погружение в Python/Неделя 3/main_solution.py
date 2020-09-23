# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 12:11:49 2020

@author: Govor_000
"""

from solution import FileReader
reader = FileReader('not_exist_file.txt')
text = reader.read() # ''
print('text_1',text)

with open('some_file.txt', 'w') as file:
     file.write('some text')

reader = FileReader('some_file.txt')
text = reader.read()
print('text_2',text) # 'some text'
print(type(reader)) # <class 'solution.FileReader'>
