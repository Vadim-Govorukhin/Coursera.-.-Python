import pygame
import random
import yaml
import os
import Objects

OBJECT_TEXTURE = os.path.join("texture", "objects")
ENEMY_TEXTURE = os.path.join("texture", "enemies")
ALLY_TEXTURE = os.path.join("texture", "ally")


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


def reload_game(engine, hero, end=False):
    global level_list
    level_list_max = len(level_list) - 1
    engine.level += 1
    hero.position = [1, 1]
    engine.objects = []
    engine.map_position = [0, 0]
    if not end:
        generator = level_list[min(engine.level, level_list_max)]
    else:
        generator = level_list[level_list_max]
    _map, _mini_map = generator['map'].get_map()
    engine.load_map(_map, _mini_map)
    engine.add_objects(generator['obj'].get_objects(_map))
    engine.add_hero(hero)
    

def restore_hp(engine, hero):
    engine.score += 0.1
    hero.hp = hero.max_hp
    engine.notify("HP restored")


# =======================================================================================
# Функции для применения бафов и дебафов
# =======================================================================================
def apply_blessing(engine, hero):
    need_gold = int(20 * 1.5**engine.level) - 2 * hero.stats["intelligence"]
    if hero.gold >= need_gold:
        engine.score += 0.2
        hero.gold -= need_gold
        if random.randint(0, 1) == 0:
            engine.hero = Objects.Blessing(hero)
            engine.notify("Blessing applied")
        else:
            engine.hero = Objects.Berserk(hero)
            engine.notify("Berserk applied")
        engine.hero.calc_max_HP()
    else:
        engine.score -= 0.1
        engine.notify(f"Need {need_gold} gold")

# Не знаю, как это отбалансить
def apply_weakness(engine, hero, *args):
    engine.hero = Objects.Weakness(hero)
    engine.hero.calc_max_HP()
    if hero.hp > hero.max_hp:
        hero.hp = hero.max_hp
    engine.notify("You were Weaknessed!")

def apply_curse(engine, hero, *args):
    engine.hero = Objects.Curse(hero)
    engine.hero.calc_max_HP()
    if hero.hp > hero.max_hp:
        hero.hp = hero.max_hp
    engine.notify("You were Cursed!")

def apply_evileye(engine, hero, *args):
    engine.hero = Objects.EvilEye(hero)
    engine.hero.calc_max_HP()
    if hero.hp > hero.max_hp:
        hero.hp = hero.max_hp
    engine.notify("You were EvilEyeed!")


# =======================================================================================
# Новый союзник
# =======================================================================================
def change_base(obj, engine):
    if isinstance(obj, Objects.Weakness) \
    or isinstance(obj, Objects.Curse) \
    or isinstance(obj, Objects.EvilEye):
        engine.notify(f"{str(obj).split(' ')[0].split('.')[1]} removed")                
        obj = obj.base
    else:
        obj.base = change_base(obj.base, engine)
    return  obj 

def remove_effect(engine, hero):
    """ Удаляет последний НЕГАТИВНЫЙ эффект"""
    need_gold = int(10 * 1.5**engine.level) - 2 * hero.stats["intelligence"]
    if hero.gold >= need_gold and "base" in dir(hero):
        hero.gold -= need_gold
        if len(hero.get_negative_effects()) >= 1:
            hero = change_base(hero, engine)
            engine.hero = hero
        else:
            engine.notify("No negative effects")    
            
        print('Положительные эффекты на герое', hero.get_positive_effects())
        print('Отрицательные эффекты на герое', hero.get_negative_effects())            
        engine.hero.calc_max_HP()
        if hero.hp > hero.max_hp:
            hero.hp = hero.max_hp   
    else:
        if "base" not in dir(hero):
            engine.notify("No any effects")
        else:
            engine.notify(f"Need {need_gold} gold")

def add_gold(engine, hero):
    if random.randint(1, 10) == 1:
        engine.score -= 0.05
        engine.hero = Objects.Weakness(hero)
        engine.notify("You were Weakness")
    else:
        engine.score += 0.1
        gold = int(random.randint(10, 1000) * (1.1**(engine.hero.level - 1)))
        hero.gold += gold
        engine.notify(f"{gold} gold added")

def fighting(engine, hero, enemy):
    """Система боёвки с врагами"""
    engine.score += 0.1
    
    # Показатель атаки вычисляется на основе силы с модификатором в виде удачи
    enemy_atack = enemy.stats["strength"]
    if random.randint(0,10) < enemy.stats['luck']:
        enemy_atack += random.randint(enemy.stats['luck'], 2*enemy.stats['luck'])
    
    hero_atack = hero.stats["strength"]
    if random.randint(0,10) < hero.stats['luck']:
        hero_atack += random.randint(hero.stats['luck'], 2*hero.stats['luck'])
    
    # Не придумал, как сбалансировать очередность ударов 
    flag = True
    while flag:
        
        #####
        if hero.stats['endurance'] >= enemy.stats['endurance']:
            enemy.hp -= hero_atack
            hero.hp -= enemy_atack
        else:
            hero.hp -= enemy_atack
            enemy.hp -= hero_atack
        if enemy.hp <= 0:
            flag = False
        if hero.hp <= 0:
            engine.notify("You defeated!")
            reload_game(engine, hero, end=True)
            break
    else:
        engine.notify("Enemy defeated!")
        hero.exp += enemy.exp
        hero.level_up(engine)
    
    
class MapFactory(yaml.YAMLObject):
    
    @classmethod
    def from_yaml(cls, loader, node):
        # сначала опишем функции для обработки каждого нового типа
        # метод loader.construct_mapping() формирует из содержания node словарь

        # обработчик создания отчёта !easy_level
        data = loader.construct_mapping(node)
        # Получаем размер карты, если она есть
        
        map_size = data.pop('size', '41x41')
        map_size = list(map(int, map_size.split('x')))
        # необходимо выбрать из полученные данных необходимые
        # для создания экземпляра класса ExampleClass
        _obj = cls.Objects()
        _obj.config = data
        _map = cls.Map(map_size)
        # FIXME
        # get _map and _obj
        return {'map': _map, 'obj': _obj}
    
    def create_map(self):
        print('In Service call create_map')
        
    def create_objects(self):
        print('In Service call create_objects')

    @classmethod        
    def create_mini_map(cls, obj):
        return [[
                            int(i==wall) for i in obj.Map[j]
                         ] for j in range(len(obj.Map))]

class EndMap(MapFactory):

    yaml_tag = "!end_map"

    class Map:
        def __init__(self, map_size=None): # map_size не используется
            self.Map = ['000000000000000000000000000000000000000',
                        '0                                     0',
                        '0                                     0',
                        '0  0   0   000   0   0  00000  0   0  0',
                        '0  0  0   0   0  0   0  0      0   0  0',
                        '0  000    0   0  00000  0000   0   0  0',
                        '0  0  0   0   0  0   0  0      0   0  0',
                        '0  0   0   000   0   0  00000  00000  0',
                        '0                                   0 0',
                        '0                                     0',
                        '000000000000000000000000000000000000000'
                        ]
            self.Map = list(map(list, self.Map))
            for i in self.Map:
                for j in range(len(i)):
                    i[j] = wall if i[j] == '0' else floor1        
            self.mini_map = MapFactory.create_mini_map(self)
            
        def get_map(self):
            return self.Map, self.mini_map

    class Objects:
        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            return self.objects


class RandomMap(MapFactory):
    yaml_tag = "!random_map"

    class Map:

        def __init__(self, map_size):
            self.Map = [[0 for _ in range(map_size[0])] for _ in range(map_size[1])]
            for i in range(map_size[0]):
                for j in range(map_size[1]):
                    if i == 0 or j == 0 or i == map_size[0] - 1 or j == map_size[1] - 1:
                        self.Map[j][i] = wall
                    else:
                        self.Map[j][i] = [wall, floor1, floor2, floor3, floor1,
                                          floor2, floor3, floor1, floor2][random.randint(0, 8)]
            self.mini_map = MapFactory.create_mini_map(self)
            
        def get_map(self):
            return self.Map, self.mini_map

    class Objects:

        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            map_size = [len(_map[0]), len(_map)]
            for obj_name in object_list_prob['objects']:
                prop = object_list_prob['objects'][obj_name]
                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = (random.randint(1, map_size[0] - 2),
                             random.randint(1, map_size[1] - 2))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, map_size[0] - 2),
                                     random.randint(1, map_size[1] - 2))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, map_size[0] - 2),
                                         random.randint(1, map_size[1] - 2))

                    self.objects.append(Objects.Ally(
                        prop['sprite'], prop['action'], coord))

            for obj_name in object_list_prob['ally']:
                prop = object_list_prob['ally'][obj_name]
                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = (random.randint(1, map_size[0] - 2),
                             random.randint(1, map_size[1] - 2))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, map_size[0] - 2),
                                     random.randint(1, map_size[1] - 2))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, map_size[0] - 2),
                                         random.randint(1, map_size[1] - 2))
                    self.objects.append(Objects.Ally(
                        prop['sprite'], prop['action'], coord))

            for obj_name in object_list_prob['enemies']:
                prop = object_list_prob['enemies'][obj_name]
                for i in range(random.randint(0, 5)):
                    coord = (random.randint(1, map_size[0] - 2),
                             random.randint(1, map_size[1] - 2))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, map_size[0] - 2),
                                     random.randint(1, map_size[1] - 2))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, map_size[0] - 2),
                                         random.randint(1, map_size[1] - 2))

                    self.objects.append(Objects.Enemy(
                        prop['sprite'], prop, prop['experience'], prop['action'], coord))

            return self.objects

# FIXME
# add classes for YAML !empty_map and !special_map{}
class EmptyMap(MapFactory):
    yaml_tag = "!empty_map"
    
    class Map:

        def __init__(self, map_size):
            self.Map = [[0 for _ in range(map_size[0])] for _ in range(map_size[1])]
            for i in range(map_size[0]):
                for j in range(map_size[1]):
                    if i == 0 or j == 0 or i == map_size[0] - 1 or j == map_size[1] - 1:
                        self.Map[j][i] = wall
                    else:
                        self.Map[j][i] = [floor1, floor1, floor2, floor3, floor1,
                                          floor2, floor3, floor1, floor2][random.randint(0, 8)]
            self.mini_map = MapFactory.create_mini_map(self)
            
            
        def get_map(self):
            return self.Map, self.mini_map

    class Objects:

        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            
            map_size = [len(_map[0]), len(_map)]
            for obj_name in object_list_prob['objects']:
                prop = object_list_prob['objects'][obj_name]
                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = (random.randint(1, map_size[0] - 2),
                             random.randint(1, map_size[1] - 2))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, map_size[0] - 2),
                                     random.randint(1, map_size[1] - 2))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, map_size[0] - 2),
                                         random.randint(1, map_size[1] - 2))

                    self.objects.append(Objects.Ally(
                        prop['sprite'], prop['action'], coord))


            return self.objects
        
        
class SpecialMap(MapFactory):
    yaml_tag = "!special_map"

    class Map:

        def __init__(self, map_size):
            self.Map = [[0 for _ in range(map_size[0])] for _ in range(map_size[1])]
            for i in range(map_size[0]):
                for j in range(map_size[1]):
                    if i == 0 or j == 0 or i == map_size[0] - 1 or j == map_size[1] - 1:
                        self.Map[j][i] = wall
                    else:
                        self.Map[j][i] = [wall, floor1, floor2, floor3, floor1,
                                          floor2, floor3, floor1, floor2][random.randint(0, 8)]
            self.mini_map = MapFactory.create_mini_map(self)
            
        def get_map(self):
            return self.Map, self.mini_map

    class Objects:
        def __init__(self):
            self.objects = []
            self.config = {}

        def get_objects(self, _map):
            
            map_size = [len(_map[0]), len(_map)]
            for obj_name in object_list_prob['objects']:
                prop = object_list_prob['objects'][obj_name]
                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = (random.randint(1, map_size[0] - 2),
                             random.randint(1, map_size[1] - 2))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, map_size[0] - 2),
                                     random.randint(1, map_size[1] - 2))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, map_size[0] - 2),
                                         random.randint(1, map_size[1] - 2))
                    self.objects.append(Objects.Ally(
                        prop['sprite'], prop['action'], coord))

            for obj_name in object_list_prob['ally']:
                prop = object_list_prob['ally'][obj_name]
                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = (random.randint(1, map_size[0] - 2),
                             random.randint(1, map_size[1] - 2))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, map_size[0] - 2),
                                     random.randint(1, map_size[1] - 2))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, map_size[0] - 2),
                                         random.randint(1, map_size[1] - 2))
                    self.objects.append(Objects.Ally(
                        prop['sprite'], prop['action'], coord))
            
            for obj_name in self.config.keys():
                prop = object_list_prob['enemies'][obj_name]
                for i in range(self.config[obj_name]):
                    coord = (random.randint(1, map_size[0] - 2),
                             random.randint(1, map_size[1] - 2))
                    #coord = (3,3)
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[1]][coord[0]] == wall:
                            intersect = True
                            coord = (random.randint(1, map_size[0] - 2),
                                     random.randint(1, map_size[1] - 2))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, map_size[0] - 2),
                                         random.randint(1, map_size[1] - 2))

                    self.objects.append(Objects.Enemy(
                        prop['sprite'], prop, prop['experience'], prop['action'], coord))

            return self.objects



wall = [0]
floor1 = [0]
floor2 = [0]
floor3 = [0]


def service_init(sprite_size, full=True):
    global object_list_prob, level_list

    global wall
    global floor1
    global floor2
    global floor3

    wall[0] = create_sprite(os.path.join("texture", "wall.png"), sprite_size)
    floor1[0] = create_sprite(os.path.join("texture", "Ground_1.png"), sprite_size)
    floor2[0] = create_sprite(os.path.join("texture", "Ground_2.png"), sprite_size)
    floor3[0] = create_sprite(os.path.join("texture", "Ground_3.png"), sprite_size)

    file = open("objects.yml", "r")

    object_list_tmp = yaml.load(file.read())
    if full:
        object_list_prob = object_list_tmp

    object_list_actions = {'reload_game': reload_game,
                           'add_gold': add_gold,
                           'apply_blessing': apply_blessing,
                           'remove_effect': remove_effect,
                           'restore_hp': restore_hp,
                           'fighting': fighting,
                           'apply_weakness': apply_weakness,
                           'apply_curse': apply_curse}

    for obj in object_list_prob['objects']:
        prop = object_list_prob['objects'][obj]
        prop_tmp = object_list_tmp['objects'][obj]
        prop['sprite'][0] = create_sprite(
            os.path.join(OBJECT_TEXTURE, prop_tmp['sprite'][0]), sprite_size)
        prop['action'] = object_list_actions[prop_tmp['action']]

    for ally in object_list_prob['ally']:
        prop = object_list_prob['ally'][ally]
        prop_tmp = object_list_tmp['ally'][ally]
        prop['sprite'][0] = create_sprite(
            os.path.join(ALLY_TEXTURE, prop_tmp['sprite'][0]), sprite_size)
        prop['action'] = object_list_actions[prop_tmp['action']]

    for enemy in object_list_prob['enemies']:
        prop = object_list_prob['enemies'][enemy]
        prop_tmp = object_list_tmp['enemies'][enemy].copy()
        prop['sprite'][0] = create_sprite(
            os.path.join(ENEMY_TEXTURE, prop_tmp['sprite'][0]), sprite_size)
        
        prop['action'] = []
        for action in prop_tmp['action']:
            prop['action'].append(object_list_actions[action])

    file.close()

    if full:
        file = open("levels.yml", "r")
        level_list = yaml.load(file.read())['levels']
        level_list.append({'map': EndMap.Map(), 'obj': EndMap.Objects()})
        file.close()
    return wall