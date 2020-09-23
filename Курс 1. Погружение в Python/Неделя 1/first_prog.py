# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 16:01:26 2020

@author: Govor_000
"""

import requests

def get_location_info():
    return requests.get("https://freegeoip.app/json/").json()


#мы хотим чтобы наша программка
#работала только тогда, когда мы ее запускаем интерпретатором Python,
if __name__ == "__main__":
    print(get_location_info())