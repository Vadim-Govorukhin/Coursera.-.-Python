# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 12:07:14 2020

@author: Govor_000
"""

class FileReader:
    """Класс FileReader помогает читать из файла"""

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        try:
            with open(self.file_path) as f:
                return f.read()
        except IOError:
            return ""
        
