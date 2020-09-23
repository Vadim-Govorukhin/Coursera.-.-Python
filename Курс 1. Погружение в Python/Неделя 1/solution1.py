# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 17:23:55 2020

@author: Govor_000
"""

import sys

num = int(sys.argv[1])

n = 1
while n <= num:
    print(' '*(num-n) + '#'*n)
    n += 1