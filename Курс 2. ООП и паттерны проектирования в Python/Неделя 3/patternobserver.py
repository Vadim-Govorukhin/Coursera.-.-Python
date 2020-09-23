# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:14:54 2020

@author: Govor_000
"""

from abc import ABC, abstractmethod

# Определим абстрактного наблюдателя
class AbstractObserver(ABC):
  
    # Каждый конкретный наблюдатель должен будет реализовать метод update
    @abstractmethod
    def update(self, message):
        pass


# Определим конкретных наблюдателей
class ShortNotificationPrinter(AbstractObserver):
    
    def __init__(self):
        # Объявим множество всех полученных достижений
        self.achievements = set()
    
    def update(self, message):
        # Добавим название достижения во множество достижений
        self.achievements.add(message["title"])
    

class FullNotificationPrinter(AbstractObserver):
    
    def __init__(self):
        # Объявим список всех полученных достижений
        self.achievements = list()
    
    def update(self, message):
        # Если подобного достижения не было в списке, добавим его
        if message not in self.achievements:
            self.achievements.append(message)
            
            
# Опишем наблюдаемую систему
#class ObservableEngine(Engine):
class ObservableEngine:
    
    def __init__(self):
        # Объявим пустое множество подписчиков
        self.subscribers = set()
        
    def subscribe(self, subscriber):
        # Добавим пользователя во множество подписчиков
        self.subscribers.add(subscriber)
    
    def unsubscribe(self, subscriber):
        # Если данный подписчик присутствует в списке подписчиков, его можно удалить
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)
    
    def notify(self, message):
        # Отправка уведомления всем подписчикам
        for subscriber in self.subscribers:
            subscriber.update(message)