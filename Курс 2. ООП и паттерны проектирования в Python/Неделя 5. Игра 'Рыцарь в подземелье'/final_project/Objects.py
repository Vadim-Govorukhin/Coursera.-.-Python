from abc import ABC, abstractmethod
import pygame
import random


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass

class AbstractObject(ABC): #####
    
    @abstractmethod
    def __init__(self,):
        pass
    
    def draw(self, display):
        min_x = self.position[0] - 1
        min_y = self.position[1] - 1
        min_x = display.engine.map_position[0]
        min_y = display.engine.map_position[1]

        display.blit(self.sprite, ((self.position[0] - min_x) * display.engine.sprite_size,
                                   (self.position[1] - min_y) * display.engine.sprite_size))
    
class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)

class Enemy(AbstractObject, Interactive):

    def __init__(self, icon, stats, exp, action, position):
        self.sprite = icon
        self.stats = stats
        self.position = list(position)
        self.exp = exp
        self.calc_max_HP()
        self.hp = self.max_hp
        self.actions = action

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2

    def interact(self, engine, hero):
        for action in self.actions:
            action(engine, hero, self)
                
    def move(self, mini_map, hero_position):
        """
        Функция реализует движение врагов на случайную клетку floor, при этом
        если враг видит героя, то враг идет в сторону героя
        """
        possible_steps = [(1,0), (0,1), (-1,0), (0,-1), (0,0)]
        dx, dy = random.choice(possible_steps)
        visible_range = [12, 12]
        visible_box = [range(self.position[0] - visible_range[0],
                             self.position[0] + visible_range[0] + 1),
                       range(self.position[1] - visible_range[1],
                             self.position[1] + visible_range[1] + 1)]
                       
        if hero_position[0] in visible_box[0] and hero_position[1] in visible_box[1]:
            # Если герой в зоне видимости, то нападение
            
            start_distance = Enemy.distance(self.position, hero_position)
            next_distance = Enemy.distance([self.position[0] + dx, 
                                            self.position[1] + dy], hero_position)
            tried_steps = set()
            while tried_steps != set(possible_steps):
                if mini_map[self.position[1] + dy][self.position[0] + dx] == 0 \
                    and next_distance < start_distance:
                        break
                dx, dy = random.choice(possible_steps)
                tried_steps.add((dx, dy))
                next_distance = Enemy.distance([self.position[0] + dx, self.position[1] + dy], hero_position)
            else:
                # Если невозможно напасть из данного положения (комната вида |_| )
                while mini_map[self.position[1] + dy][self.position[0] + dx] == 1:
                    dx, dy = random.choice(possible_steps)
            
        else:
            while mini_map[self.position[1] + dy][self.position[0] + dx] == 1:
                dx, dy = random.choice(possible_steps)

        self.position[0] += dx
        self.position[1] += dy
        
    @staticmethod
    def distance(point_1, point_2):
        """ Манхетенское расстояние """
        return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])

class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2


class Hero(Creature):

    def __init__(self, stats, icon):
        self.positive_effects = []
        self.negative_effects = []
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self, engine):
        if self.exp >= 100 * (2 ** (self.level - 1)):
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp
            engine.notify("Level up!")
        
    def get_positive_effects(self):
        return self.positive_effects

    def get_negative_effects(self):
        return self.negative_effects
    
class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        pass

    def get_negative_effects(self):
        return self.base.get_negative_effects()
    
    def get_positive_effects(self):
        return self.base.get_positive_effects()
    
# =======================================================================================
# Бафы
# =======================================================================================
class Berserk(Effect):
    """
    Увеличивает характеристики: Сила, Выносливость, Ловкость, Удача на 7;
    уменьшает характеристики: Восприятие, Харизма, Интеллект на 3;
    количество единиц здоровья увеличивается на 50.
    """
    
    def apply_effect(self):
        # Получим характеристики базового объекта, модифицируем их и вернем
        #stats = self.stats
        """
        increasing_stats = ["strength", "endurance", "agility", "luck"]
        decreasing_stats = ["perception", "charisma", "intelligence"]
        """
        increasing_stats = ["strength", "endurance", "luck"]
        decreasing_stats = ["intelligence"]
        for key in self.stats.keys():
            if key in increasing_stats:
                self.stats[key] += 7
            elif key in decreasing_stats:
                self.stats[key] -= 3
            elif key == 'HP':
                self.stats[key] += 50
      
    def get_positive_effects(self):
        # Модифицируем список эффектов, добавив в него новый эффект
        return self.base.get_positive_effects() + [self.__class__.__name__]
    
class Blessing(Effect):
    """увеличивает все основные характеристики на 2"""
    
    def apply_effect(self):
        """
        main_stats = ["strength", "perception", "endurance", "charisma",
                      "intelligence", "agility", "luck"]
        """
        main_stats = ["strength", "endurance",
                      "intelligence", "luck"]
        for key in main_stats:
            self.stats[key] += 2
            
    def get_positive_effects(self):
        # Модифицируем список эффектов, добавив в него новый эффект
        return self.base.get_positive_effects() + [self.__class__.__name__]
        
# =======================================================================================
# Дебафы
# =======================================================================================
class Weakness(Effect):
    """уменьшает характеристики: Сила, Выносливость, Ловкость на 4"""
    
    def apply_effect(self):
        """
        decreasing_stats = ["strength", "endurance", "agility"]
        """
        decreasing_stats = ["strength", "endurance"]
        for key in decreasing_stats:
            self.stats[key] -= 4

    def get_negative_effects(self):
        return self.base.get_negative_effects() + [self.__class__.__name__]

class Curse(Effect):
    """уменьшает все основные характеристики на 2"""
    
    def apply_effect(self):
        """
        main_stats = ["strength", "perception", "endurance", "charisma",
                      "intelligence", "agility", "luck"]
        """
        main_stats = ["strength", "endurance", 
                      "intelligence", "luck"]
        for key in main_stats:
            self.stats[key] -= 2

    def get_negative_effects(self):
        return self.base.get_negative_effects() + [self.__class__.__name__]

    
class EvilEye(Effect):
    """уменьшает  характеристику Удача на 10"""
    
    def apply_effect(self):
        self.stats["Luck"] -= 10
        
    def get_negative_effects(self):
        return self.base.get_negative_effects() + [self.__class__.__name__]
