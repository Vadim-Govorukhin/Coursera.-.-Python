# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 17:16:41 2020

@author: Govor_000
"""

import sys

digit_string = sys.argv[1]

sum = 0
for letter in digit_string:
    sum +=int(letter)
print(sum)

print(sum([int(x) for x in sys.argv[1]]))