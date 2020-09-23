#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)

class Vec2d:
    
    def __init__(self,x,y):
        self.coordinates = (x,y)
    
    def __sub__(self, vector):
        """возвращает разность двух векторов"""
        return Vec2d(self.coordinates[0] - vector.coordinates[0],
                     self.coordinates[1] - vector.coordinates[1])

    def __add__(self, vector):
        """возвращает сумму двух векторов"""
        return Vec2d(self.coordinates[0] + vector.coordinates[0],
                     self.coordinates[1] + vector.coordinates[1]) 
        
    def len(self):
        """возвращает длину вектора"""
        return math.sqrt(self.coordinates[0] * self.coordinates[0] 
                       + self.coordinates[1] * self.coordinates[1])
        
    def __mul__(self, k):
        """возвращает произведение вектора на число"""
        return Vec2d(self.coordinates[0] * k, self.coordinates[1] * k)
        
    def int_pair(self):
        """возвращает пару координат, определяющих вектор (координаты точки конца вектора),
        координаты начальной точки вектора совпадают с началом системы координат (0, 0)"""
        return list(map(int,self.coordinates))
    
    def __getitem__(self, key):
        """возвращает координату вектора под номером key"""
        return self.coordinates[key]
   
    
# =======================================================================================
# Функции отрисовки
# =======================================================================================
        
class Polyline():
    
    def __init__(self, points=[], speeds=[]):
        self.points = points
        self.speeds = speeds
        
    def append_point(self, value):
        self.points.append(value)
        
    def append_speed(self, value):
        self.speeds.append(value)
        
    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        if style == "line":
            points = self.support_points
            #print('draw',points)
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color,
                                 points[p_n].int_pair(),
                                 points[p_n + 1].int_pair(),
                                 width)
    
        elif style == "points":
            points = self.points
            for p in points:
                pygame.draw.circle(gameDisplay, color,
                                   p.int_pair(),
                                   width)
                
    def set_points(self):
        """функция перерасчета координат опорных точек"""
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p][0] > SCREEN_DIM[0] or self.points[p][0] < 0:
                self.speeds[p] = Vec2d(- self.speeds[p][0], self.speeds[p][1])
            if self.points[p][1] > SCREEN_DIM[1] or self.points[p][1] < 0:
                self.speeds[p] = Vec2d(self.speeds[p][0], -self.speeds[p][1])    
            
  
class Knot(Polyline):
    
    def __init__(self,steps=0, points=[], speeds=[]):
        super().__init__(points,speeds)
        self.support_points = []
        self.steps = steps 
        
    
    def append_point(self, value):
        Polyline.append_point(self,value)
        self.support_points = self.get_knot()
        
    def set_points(self):
        Polyline.set_points(self)
        self.support_points = self.get_knot()
        
        
    def get_knot(self):
        points = self.points
        count = self.steps
        if len(points) < 3:
            return []
        res = []
        for i in range(-2, len(points) - 2):
            ptn = []
            ptn.append((points[i] + points[i + 1])*0.5)
            ptn.append(points[i + 1])
            ptn.append((points[i + 1] + points[i + 2])*0.5)
    
            res.extend(Knot.get_points(ptn, count))
        return res
     
    # =======================================================================================
    # Функции, отвечающие за расчет сглаживания ломаной
    # =======================================================================================
    @staticmethod
    def get_point(points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg]*alpha + Knot.get_point(points, alpha, deg - 1)*(1 - alpha)
    
    @staticmethod
    def get_points(base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(Knot.get_point(base_points, i * alpha))
        return res    
    
    

def draw_help():
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    knot = Knot(steps)
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    knot = Knot()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    knot.steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    knot.steps -= 1 if knot.steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                knot.append_point(Vec2d(*event.pos))
                knot.append_speed(Vec2d(random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        
        knot.draw_points()
        knot.draw_points("line", 3, color)
        if not pause:
            knot.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
