import os
import pygame
import collections
from math import ceil # Округление вверх для миникарты
import Service
import Objects

OBJECT_TEXTURE = os.path.join("texture", "objects")
ENEMY_TEXTURE = os.path.join("texture", "enemies")
ALLY_TEXTURE = os.path.join("texture", "ally")

colors = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "red": (255, 0, 0, 255),
    "green": (0, 255, 0, 255),
    "blue": (0, 0, 255, 255),
    "wooden": (153, 92, 0, 255),
}

def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
    sprite.blit(icon, (0, 0))
    return sprite

class ScreenHandle(pygame.Surface):

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            self.successor = args[-1]
            self.next_coord = args[-2]
            args = args[:-2]
        else:
            self.successor = None
            self.next_coord = (0, 0)
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def draw(self, canvas):
        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)
            
    def update(self, value):
        if self.successor is not None:
            self.successor.update(value)

    def connect_engine(self, engine):
        if self.successor is not None:
            return self.successor.connect_engine(engine)


class GameSurface(ScreenHandle):
    
    def connect_engine(self, engine):
        """save engine and send it to next in chain"""
        self.engine = engine
        super().connect_engine(engine)
        
    def update(self, value):
        super().update(value)    

    def draw_hero(self):
        self.engine.hero.draw(self)

    def draw_map(self):
        size = self.engine.sprite_size
        # (min_x,min_y) - left top corner

        min_x = self.engine.map_position[0]
        min_y = self.engine.map_position[1]

        if self.engine.map:
            self.fill(colors["black"])
            for i in range(len(self.engine.map[0]) - min_x):
                for j in range(len(self.engine.map) - min_y):
                    self.blit(self.engine.map[min_y + j][min_x + i][
                              0], (i * size, j * size))
        else:
            self.fill(colors["white"])

    def draw_object(self, sprite, coord):
        size = self.engine.sprite_size
        # (min_x,min_y) - left top corner

        min_x = self.engine.map_position[0]
        min_y = self.engine.map_position[1]
        self.blit(sprite, ((coord[0] - min_x) * size,
                           (coord[1] - min_y) * size))

    def draw(self, canvas):
        size = self.engine.sprite_size
        # (min_x,min_y) - left top corner
        min_x = self.engine.map_position[0]
        min_y = self.engine.map_position[1]        
        
        self.draw_map()
        for obj in self.engine.objects:
            self.blit(obj.sprite[0], ((obj.position[0] - min_x) * size,
                                      (obj.position[1] - min_y) * size))
        self.draw_hero()
        super().draw(canvas)

class MiniMap(ScreenHandle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = None
        self.mini_sprite_size = 4
        self.m_wall = create_sprite(os.path.join("texture", "wall_mini.png"), self.mini_sprite_size)
        self.m_floor = create_sprite(os.path.join("texture", "Ground_mini.png"), self.mini_sprite_size)
        self.m_hero = create_sprite(os.path.join("texture", "Hero_mini.png"), self.mini_sprite_size)
        self.m_ally = create_sprite(os.path.join(ALLY_TEXTURE, 'NPC_mini.png'), self.mini_sprite_size)
        self.m_enemy = create_sprite(os.path.join(ENEMY_TEXTURE, 'enemy_mini.png'), self.mini_sprite_size)

    def connect_engine(self, engine):
        """save engine and send it to next in chain"""
        self.engine = engine
        super().connect_engine(engine)

    def draw_map(self):
        if self.engine.map:
            for i in range(len(self.engine.map[0])):
                for j in range(len(self.engine.map)):
                    if self.engine.map[j][i] == Service.wall:
                        self.blit(self.m_wall, (i * self.mini_sprite_size, j * self.mini_sprite_size))
                    else:
                        self.blit(self.m_floor, (i * self.mini_sprite_size, j * self.mini_sprite_size))
        else:
            self.fill(colors["white"])

    def draw(self, canvas):
        self.fill((0, 0, 0, 0))
        if self.engine.show_mini_map:
            self.draw_map()

            for obj in self.engine.objects:
                if obj != {}:
                    if isinstance(obj, Objects.Ally):
                        self.blit(self.m_ally, ((obj.position[0]) * self.mini_sprite_size,
                                                (obj.position[1]) * self.mini_sprite_size))
                    elif isinstance(obj, Objects.Enemy):
                        self.blit(self.m_enemy, ((obj.position[0]) * self.mini_sprite_size,
                                                  (obj.position[1]) * self.mini_sprite_size))

            self.blit(self.m_hero, (self.engine.hero.position[0] * self.mini_sprite_size,
                                    self.engine.hero.position[1] * self.mini_sprite_size))

        # отрисовка следующей поверхности в цепочке
        super().draw(canvas)
        
class ProgressBar(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def connect_engine(self, engine):
        self.engine = engine
        super().connect_engine(engine)
        
    def update(self, value):
        super().update(value)
        
    def draw(self, canvas):
        self.fill(colors["wooden"])
        pygame.draw.rect(self, colors["black"], (50, 30, 200, 30), 2)
        pygame.draw.rect(self, colors["black"], (50, 70, 200, 30), 2)

        pygame.draw.rect(self, colors[
                         "red"], (50, 30, 200 * self.engine.hero.hp / self.engine.hero.max_hp, 30))
        pygame.draw.rect(self, colors["green"], (50, 70,
                                                 200 * self.engine.hero.exp / (100 * (2**(self.engine.hero.level - 1))), 30))

        font = pygame.font.SysFont("comicsansms", 20)
        self.blit(font.render(f'Hero at {self.engine.hero.position}', True, colors["black"]),
                  (250, 0))

        self.blit(font.render(f'{self.engine.level} floor', True, colors["black"]),
                  (10, 0))

        self.blit(font.render('HP', True, colors["black"]),
                  (10, 30))
        self.blit(font.render('Exp', True, colors["black"]),
                  (10, 70))

        self.blit(font.render(f'{self.engine.hero.hp}/{self.engine.hero.max_hp}', True, colors["black"]),
                  (60, 30))
        self.blit(font.render(f'{self.engine.hero.exp}/{(100*(2**(self.engine.hero.level-1)))}', True, colors["black"]),
                  (60, 70))

        self.blit(font.render('Level', True, colors["black"]),
                  (300, 30))
        self.blit(font.render('Gold', True, colors["black"]),
                  (300, 70))

        self.blit(font.render(f'{self.engine.hero.level}', True, colors["black"]),
                  (360, 30))
        self.blit(font.render(f'{self.engine.hero.gold}', True, colors["black"]),
                  (360, 70))

        self.blit(font.render('Str', True, colors["black"]),
                  (420, 30))
        self.blit(font.render('Luck', True, colors["black"]),
                  (420, 70))

        self.blit(font.render(f'{self.engine.hero.stats["strength"]}', True, colors["black"]),
                  (480, 30))
        self.blit(font.render(f'{self.engine.hero.stats["luck"]}', True, colors["black"]),
                  (480, 70))

        self.blit(font.render('SCORE', True, colors["black"]),
                  (550, 30))
        self.blit(font.render(f'{self.engine.score:.4f}', True, colors["black"]),
                  (550, 70))
        
        super().draw(canvas)


class InfoWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)

    def update(self, value):
        self.data.append(f"> {str(value)}")
        super().update(value)        

    def draw(self, canvas):
        self.fill(colors["wooden"])
        font = pygame.font.SysFont("comicsansms", 18)
        for i, text in enumerate(self.data):
            self.blit(font.render(text, True, colors["black"]),
                      (-5, 18 * i))
        super().draw(canvas)

    def connect_engine(self, engine):
        self.engine = engine
        super().connect_engine(engine)
        

class HelpWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)
        self.data.append([" →", "Move Right"])
        self.data.append([" ←", "Move Left"])
        self.data.append([" ↑ ", "Move Top"])
        self.data.append([" ↓ ", "Move Bottom"])
        self.data.append([" w", "Move Map Right"])
        self.data.append([" a", "Move Map Left"])
        self.data.append([" s ", "Move Map Top"])
        self.data.append([" d ", "Move Map Bottom"])
        self.data.append([" H ", "Show Help"])
        self.data.append([" M ", "Show MiniMap"])
        self.data.append(["Num+", "Zoom +"])
        self.data.append(["Num-", "Zoom -"])
        self.data.append([" R ", "Restart Game"])
    # FIXME You can add some help information

    def connect_engine(self, engine):
        self.engine = engine
        super().connect_engine(engine)
    def update(self, value):
        pass
    
    
    def draw(self, canvas):
        alpha = 0
        if self.engine.show_help:
            alpha = 128
        self.fill((0, 0, 0, alpha))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        if self.engine.show_help:
            pygame.draw.lines(self, (255, 0, 0, 255), True, [
                              (0, 0), (700, 0), (700, 500), (0, 500)], 5)
            for i, text in enumerate(self.data):
                self.blit(font1.render(text[0], True, ((128, 128, 255))),
                          (50, 50 + 30 * i))
                self.blit(font2.render(text[1], True, ((128, 128, 255))),
                          (150, 50 + 30 * i))
                
        super().draw(canvas)
