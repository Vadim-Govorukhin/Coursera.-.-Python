# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 13:34:23 2020

@author: Govor_000
"""


from abc import ABC, abstractmethod
"""
class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        self.stats = {
            "HP": 128,  # health points
            "MP": 42,  # magic points, 
            "SP": 100,  # skill points
            "Strength": 15,  # сила
            "Perception": 4,  # восприятие
            "Endurance": 8,  # выносливость
            "Charisma": 2,  # харизма
            "Intelligence": 3,  # интеллект
            "Agility": 8,  # ловкость 
            "Luck": 1  # удача
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()
 """   
    
class AbstractEffect(ABC, Hero):
    
    def __init__(self, base):
        self.base = base

    @abstractmethod
    def get_stats(self):
        pass
    
    @abstractmethod
    def get_positive_effects(self):
        return self.positive_effects

    @abstractmethod
    def get_negative_effects(self):
        return self.negative_effects 
    
# В AbstractPositive будем возвращать список наложенных отрицательных эффектов
# без изменений, чтобы не определять данный метод во всех положительных эффектах
class AbstractPositive(AbstractEffect):
    
    def get_negative_effects(self):
        return self.base.get_negative_effects()

# =======================================================================================
# Бафы
# =======================================================================================
class Berserk(AbstractPositive):
    """
    Увеличивает характеристики: Сила, Выносливость, Ловкость, Удача на 7;
    уменьшает характеристики: Восприятие, Харизма, Интеллект на 3;
    количество единиц здоровья увеличивается на 50.
    """
    
    def get_stats(self):
        # Получим характеристики базового объекта, модифицируем их и вернем
        stats = self.base.get_stats()
        
        increasing_stats = ["Strength", "Endurance", "Agility", "Luck"]
        decreasing_stats = ["Perception", "Charisma", "Intelligence"]
        for key in stats.keys():
            if key in increasing_stats:
                stats[key] += 7
            elif key in decreasing_stats:
                stats[key] -= 3
            elif key == 'HP':
                stats[key] += 50
        return stats

    def get_positive_effects(self):
        # Модифицируем список эффектов, добавив в него новый эффект
        return self.base.get_positive_effects() + [self.__class__.__name__]
    

class Blessing(AbstractPositive):
    """увеличивает все основные характеристики на 2"""
    
    def get_stats(self):
        stats = self.base.get_stats()
        main_stats = ["Strength", "Perception", "Endurance", "Charisma",
                      "Intelligence", "Agility", "Luck"]
        for key in main_stats:
            stats[key] += 2
        return stats

    def get_positive_effects(self):
        return self.base.get_positive_effects() + [self.__class__.__name__]


# Для отрицательных эффектов неизменным останется список положительных эффектов
class AbstractNegative(AbstractEffect):
    
    def get_positive_effects(self):
        return self.base.get_positive_effects()
    
# =======================================================================================
# Дебафы
# =======================================================================================
class Weakness(AbstractNegative):
    """уменьшает характеристики: Сила, Выносливость, Ловкость на 4"""
    
    def get_stats(self):
        stats = self.base.get_stats()
        decreasing_stats = ["Strength", "Endurance", "Agility"]
        for key in decreasing_stats:
            stats[key] -= 4
        return stats

    def get_negative_effects(self):
        return self.base.get_negative_effects() + [self.__class__.__name__]


class Curse(AbstractNegative):
    """уменьшает все основные характеристики на 2"""
    
    def get_stats(self):
        stats = self.base.get_stats()
        main_stats = ["Strength", "Perception", "Endurance", "Charisma",
                      "Intelligence", "Agility", "Luck"]
        for key in main_stats:
            stats[key] -= 2
        return stats

    def get_negative_effects(self):
        return self.base.get_negative_effects() + [self.__class__.__name__]
    

class EvilEye(AbstractNegative):
    """уменьшает  характеристику Удача на 10"""
    
    def get_stats(self):
        stats = self.base.get_stats()
        stats["Luck"] -= 10
        return stats

    def get_negative_effects(self):
        return self.base.get_negative_effects() + [self.__class__.__name__]
    
    
    
"""
hero = Hero()
print(hero.get_negative_effects())
print(hero.get_positive_effects())
print(hero.get_stats())

print('*'*10)
ee1 = EvilEye(hero)
print(hero.get_negative_effects())
print(ee1.get_negative_effects())
print(ee1.get_positive_effects())
print(ee1.get_stats())

print('*'*10)
ee2 = EvilEye(ee1)
print(hero.get_negative_effects())
print(ee2.get_negative_effects())
print(ee2.get_positive_effects())
print(ee2.get_stats())

print('*'*10)
brs1 = Berserk(ee2)
print(hero.get_negative_effects())
print(brs1.get_negative_effects())
print(brs1.get_positive_effects())
print(brs1.get_stats())
"""





