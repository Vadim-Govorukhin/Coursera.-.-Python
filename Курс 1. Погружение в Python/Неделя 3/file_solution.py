# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 16:01:36 2020

@author: Govor_000
"""

import os
import tempfile
import uuid

class File:
    
    def __init__(self, path_to_file):
        self.current_position = 0
        self.path_to_file = path_to_file
        if not os.path.exists(path_to_file):
            open(path_to_file, "w").close()
    
    def __add__(self,file_obj):
        new_file_name = os.path.basename(self.path_to_file) \
                      + os.path.basename(file_obj.path_to_file)
        new_file = File(os.path.join(tempfile.gettempdir(), new_file_name))
        
        """
        # мы генерим имя с помощью модуля uuid, который позволяет создавать идентификаторы UUID.        
        new_path = os.path.join(
            os.path.dirname(self.path),
            str(uuid.uuid4().hex)
        )
        
        new_file = type(self)(new_path)
        """
        
        new_file.write(self.read() + file_obj.read())

        return new_file

    def __str__(self):
        return self.path_to_file
        
    def __iter__(self):
        return self
    
    def __next__(self):
        with open(self.path_to_file, "r") as f:
            f.seek(self.current_position)

            line = f.readline()
            if not line:
                self.current_position = 0
                raise StopIteration('EOF')

            return line
        
    def read(self,):
        with open(self.path_to_file, "r") as f:
            return f.read()
            
    def write(self, text):
        with open(self.path_to_file, "w") as f:
            f.write(text)
    



"""
path_to_file = 'some_filename'
os.path.exists(path_to_file) # False
file_obj = File(path_to_file)
os.path.exists(path_to_file) # True
file_obj.read() # ''
file_obj.write('some text') # 9
file_obj.read() # 'some text'
file_obj.write('other text') # 10
file_obj.read() #'other text'

file_obj_1 = File(path_to_file + '_1')
file_obj_2 = File(path_to_file + '_2')
file_obj_1.write('line 1\n') # 7
file_obj_2.write('line 2\n') # 7
new_file_obj = file_obj_1 + file_obj_2
isinstance(new_file_obj, File) # True

"""