# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 17:30:03 2020

@author: Govor_000
"""

import sys 
a = int(sys.argv[1]) 
b = int(sys.argv[2]) 
c = int(sys.argv[3])

D = b ** 2 - 4*a*c
x1 = (-b + D ** 0.5)/(2*a)
x2 = (-b - D ** 0.5)/(2*a)
print(int(x1),int(x2),sep='\n')