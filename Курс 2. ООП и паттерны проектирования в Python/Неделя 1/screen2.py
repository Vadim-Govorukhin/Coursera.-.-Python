# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 11:55:08 2020

@author: Govor_000
"""

import math
import random

import pygame

SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, x, y):
       self.x = x
       self.y = y

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)
    
    def __mul__(self, k):
        return Vec2d(self.x*k, self.y*k)
    
    def __len__(self):
        return math.sqrt(self.x**2 + self.y**2)

    def int_pair(self):  # Ð²Ð°Ñ‰Ðµ Ñ…Ð· Ð·Ð°Ñ‡ÐµÐ¼ ÑÑ‚Ð¾
        return (self.x, self.y)


class Polyline:
    def __init__(self):
        self.points = []
        self.speeds = []

    def append(self, x, y):
        '''Adds new point with random speed'''
        self.points.append(Vec2d(x, y))
        self.speeds.append(Vec2d(random.random(), random.random()))
    
    def pop(self):
        '''Delete last point'''
        if len(self.points) > 0:
            self.points.pop()
            self.speeds.pop()

    def set_points(self):
        """Ñ„ÑƒÐ½ÐºÑ†Ð¸Ñ Ð¿ÐµÑ€ÐµÑ€Ð°ÑÑ‡ÐµÑ‚Ð° ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚ Ð¾Ð¿Ð¾Ñ€Ð½Ñ‹Ñ… Ñ‚Ð¾Ñ‡ÐµÐº"""
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p].x = -self.speeds[p].x
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p].y = -self.speeds[p].y 


class Knot(Polyline):
    def __init__(self, steps=35):
        super().__init__()
        self.steps = steps
    
    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        
        return points[deg] * alpha + self.get_point(points, alpha, deg-1) * (1-alpha)

    def get_points(self, base_points):
        alpha = 1 / self.steps
        res = []
        for i in range(self.steps):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            res.extend(self.get_points(ptn))
        return res

    def change_speed(self, num):
        '''Change speed of knots by koef'''
        for i in range(len(self.speeds)):
            self.speeds[i] *= num

class Game:
    def __init__(self):
        self.display = pygame.display.set_mode(SCREEN_DIM)
        
    def draw_points(self, points, style="points", width=3, color=(255, 255, 255)):
        """Ñ„ÑƒÐ½ÐºÑ†Ð¸Ñ Ð¾Ñ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ¸ Ñ‚Ð¾Ñ‡ÐµÐº Ð½Ð° ÑÐºÑ€Ð°Ð½Ðµ"""
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(self.display, color,
                                (int(points[p_n].x), int(points[p_n].y)),
                                (int(points[p_n + 1].x), int(points[p_n + 1].y)), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(self.display, color,
                                (int(p.x), int(p.y)), width)


    def draw_help(self):
        """Ñ„ÑƒÐ½ÐºÑ†Ð¸Ñ Ð¾Ñ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ¸ ÑÐºÑ€Ð°Ð½Ð° ÑÐ¿Ñ€Ð°Ð²ÐºÐ¸ Ð¿Ñ€Ð¾Ð³Ñ€Ð°Ð¼Ð¼Ñ‹"""
        self.display.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = [
            ["F1", "Show Help"],
            ["R", "Restart"],
            ["P", "Pause/Play"],
            ["Num+", "More points"],
            ["Num-", "Less points"],
            ["Left mouse button", "Add point to knot"],
            ["Right mouse button", "Delete last point"],
            ["Mouse wheel down", "Prev knot"],
            ["Mouse wheel up", "Next knot"],
            ["Q", "Speed++"],
            ["W", "Speed--"]
        ]

        pygame.draw.lines(self.display, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.display.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.display.blit(font2.render(
                text[1], True, (128, 128, 255)), (400, 100 + 30 * i))
    
    def draw_knot_num(self, num, step):
        '''Short Info bar'''
        font = pygame.font.SysFont("courier", 24)
        texts = [
            f'Current knot: {num}',
            f'Current step: {step}'
        ]
        for i in range(2):
            self.display.blit(
                font.render(texts[i], True, (156, 221, 132)),
                (0, i * 50, 100, 100)
            )


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("MyScreenSaver")

    working = True
    knots = [Knot()]  # <---------------------------------Array of knots: Mouse wheel up to add
    cur_knot = 0      # Current using index of knot
    game = Game()
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
                    knots = [Knot()]
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_q:
                    knots[cur_knot].change_speed(1.1)
                if event.key == pygame.K_w:
                    knots[cur_knot].change_speed(0.9)
                if event.key == pygame.K_KP_PLUS:
                    knots[cur_knot].steps += 1 
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS and knots[cur_knot].steps > 1:
                    knots[cur_knot].steps -= 1 

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    knots[cur_knot].append(*event.pos)
                if event.button == 3:
                    knots[cur_knot].pop()
                if event.button == 4:
                    if cur_knot == len(knots) - 1:
                        if len(knots[cur_knot].points) == 0:
                            continue
                        else:
                            knots.append(Knot())
                    cur_knot += 1

                if event.button == 5 and cur_knot > 0:
                    cur_knot -= 1

        hue = (hue + 1) % 360
        game.display.fill((0, 0, 0))
        
        for i in range(len(knots)):
            color.hsla = (hue, ((i+1) * 11)%100, ((i+1) * 24)%100, ((i+1)*459)%100)
            if i == cur_knot:
                color.r = 255
                color.g = 0
                color.b = 0
            game.draw_points(knots[i].points)
            game.draw_points(knots[i].get_knot(), "line", 3, color)
            if not pause:
                knots[i].set_points()
        if show_help:
            game.draw_help()
        game.draw_knot_num(cur_knot, knots[cur_knot].steps)
        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)