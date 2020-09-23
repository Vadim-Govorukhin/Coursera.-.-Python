# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 12:26:20 2020

@author: Govor_000
"""
import os
import re
import csv

class CarBase:
    
    
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name 
        self.carrying = float(carrying.replace(',','.'))
        
        
    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]

class Car(CarBase):
    
    
     def __init__(self, brand, photo_file_name, carrying,
                 passenger_seats_count):
        super().__init__(brand, photo_file_name,  carrying)
        self.car_type = 'car'
        self.passenger_seats_count = int(passenger_seats_count)

    
    
class Truck(CarBase):
    
    
    def __init__(self, brand, photo_file_name, carrying,
                 body_whl):
        super().__init__(brand, photo_file_name,  carrying)
        self.car_type = 'truck'
        match = re.fullmatch(r'\d+(\.\d+)?(?:x\d+(\.\d+)?){2}',body_whl)
        self.body_length, self.body_width, self.body_height \
                    = map(float,body_whl.split('x')) if match else (0.,0.,0.) 
    
    
    def get_body_volume(self,):
        return self.body_length * self.body_width * self.body_height
    
class SpecMachine(CarBase):
    
    
    def __init__(self, brand, photo_file_name, carrying,
                 extra):
        super().__init__(brand, photo_file_name,  carrying)
        self.car_type = 'spec_machine'
        self.extra = extra
    
    
def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            print(row)
            # Обработка невалидных данных
            if len(row)== 0 or os.path.splitext(row[3])[1] not in ['.jpg', '.jpeg', '.png', '.gif'] \
                or row[1] == '':
                continue
            
            try:
                float(row[5].replace(',','.'))
            except ValueError:
                print('here',row[5])
                continue
            
            if row[0] == 'car':
                try:
                    int(row[2])
                except ValueError:
                    continue
                
                car_list.append(Car(row[1], row[3], row[5], row[2]))
                
            elif row[0] == 'truck':
                car_list.append(Truck(row[1], row[3], row[5], row[4]))
                
            elif row[0] == 'spec_machine':
                if len(row[6]) == 0:
                    continue
                car_list.append(SpecMachine(row[1], row[3], row[5], row[6]))

            else:
                continue;
            #"""
                
    
    return car_list 






    
    