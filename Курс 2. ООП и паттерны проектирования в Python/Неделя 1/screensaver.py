#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

from abc import ABC, abstractmethod

class BaseHelpWindow(ABC):
    @abstractmethod
    def draw_help(self, *args, **kwargs):
        pass


class PyHelpWindow(BaseHelpWindow):
    DARK = (50, 50, 50)
    LIGHT_BLUE = (128, 128, 255)

    def __init__(self):
        self.font1 = pygame.font.SysFont("courier", 24)
        self.font2 = pygame.font.SysFont("serif", 24)

        self.data = [["F1", "Show Help"],
                ["R", "Restart"],
                ["P", "Pause/Play"],
                ["Num+", "More points"],
                ["Num-", "Less points"],
                ["", ""],
                ["0", "Current steps"]
        ]

    def draw_help(self, *args, **kwargs):
        self.__update_data(kwargs["steps"])

        kwargs["display"].fill(self.DARK)
        pygame.draw.lines(kwargs["display"], (255, 50, 50, 255), True, 
                          [(0, 0), (800, 0), (800, 600), (0, 600)], 5
        )

        for i, text in enumerate(self.data):
            kwargs["display"].blit(self.font1.render(
                text[0], True, self.LIGHT_BLUE), (100, 100 + 30 * i)
            )

            kwargs["display"].blit(self.font2.render(
                text[1], True, self.LIGHT_BLUE), (200, 100 + 30 * i)
            )

    def __update_data(self, steps):
        self.data[-1][0] = str(steps)


class Canvas:
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def draw_points(self):
        pass

    @abstractmethod
    def update_points(self):
        pass

    @abstractmethod
    def add_point(self):
        pass

    @abstractmethod
    def quit(self):
        pass


class PyGameCanvas(Canvas):
    SCREEN_DIM = (800, 600)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self):
        pygame.init()

        self.steps = 35
        self.working = True
        self.is_show_help = False
        self.is_pause = True
        self.hue = 0
        self.color = pygame.Color(0)

        self.polyline = Polyline()
        self.knot = Knot()
        self.help_window = PyHelpWindow()

        self.gameDisplay = pygame.display.set_mode(self.SCREEN_DIM)
        pygame.display.set_caption("MyScreenSaver")

    def run(self):
        while self.working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.working = False
                    if event.key == pygame.K_r:
                        self.polyline.clear()
                    if event.key == pygame.K_p:
                        self.is_pause = not self.is_pause
                    if event.key == pygame.K_KP_PLUS:
                        self.steps += 1
                    if event.key == pygame.K_F1:
                        self.is_show_help = not self.is_show_help
                    if event.key == pygame.K_KP_MINUS:
                        self.steps -= 1 if self.steps > 1 else 0

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.add_point(event)

            self.draw_scene()

            if not self.is_pause:
                self.update_points()

            if self.is_show_help:
                self.show_help()

            pygame.display.flip()

        self.quit() 


    def draw_scene(self):
        self.gameDisplay.fill(self.BLACK)
        self.hue = (self.hue + 1) % 360
        self.color.hsla = (self.hue, 100, 50, 100)

        self.polyline.draw_points(self.gameDisplay, 3, self.WHITE)
        self.knot.update_points(self.polyline.points, self.steps)
        self.knot.draw_points(self.gameDisplay, 3, self.color)

    def update_points(self):
        self.polyline.set_points(self.polyline.points, self.polyline.speeds, self.SCREEN_DIM)

    def add_point(self, event):
        self.polyline.append_point(event.pos[0], event.pos[1])
        self.polyline.append_speed(random.random() * 2, random.random() * 2)

    def show_help(self):
        self.help_window.draw_help(display=self.gameDisplay, steps=self.steps)

    def quit(self):
        pygame.display.quit()
        pygame.quit()
        exit(0)


class Vec2d:
    def __init__(self, ax, ay):
        self.ax = ax
        self.ay = ay

    def __add__(self, vec):
        return Vec2d(self.ax + vec.ax, self.ay + vec.ay)

    def __sub__(self, vec):
        return Vec2d(self.ax - vec.ax, self.ay - vec.ay)

    def __mul__(self, num):
        return Vec2d(self.ax * num, self.ay * num)

    def __len__(self):
        return math.sqrt(self.ax * self.ax + self.ay * self.ay)

    def int_pair(self):
        return (int(self.ax), int(self.ay))


class Polyline:
    def __init__(self):
        self.clear()

    def clear(self):
        self.points = []
        self.speeds = []

    def append_point(self, x, y):
        self.points.append(Vec2d(x, y))

    def append_speed(self, x, y):
        self.speeds.append(Vec2d(x, y))

    def draw_points(self, gameDisplay, width, color):
        for p in self.points:
            pygame.draw.circle(gameDisplay, color,
                               p.int_pair(), width
            )

    def set_points(self, points, speeds, SCREEN_DIM):
        for p in range(len(points)):
            points[p] = points[p] + speeds[p]

            if points[p].ax > SCREEN_DIM[0] or points[p].ax < 0:
                speeds[p].ax = -speeds[p].ax

            if points[p].ay > SCREEN_DIM[1] or points[p].ay < 0:
                speeds[p].ay = -speeds[p].ay


class Knot(Polyline):
    def __init__(self):
        self.points = []

    def update_points(self, points, count):
        self.points = self.get_knot(points, count)

    def get_knot(self, points, count):
        if len(points) < 3:
            return []

        res = []

        for i in range(-2, len(points) - 2):
            ptn = []
            ptn.append((points[i] + points[i + 1]) * 0.5)
            ptn.append(points[i + 1])
            ptn.append((points[i + 1] + points[i + 2]) * 0.5)

            res.extend(self.__get_points(ptn, count))

        return res

    def draw_points(self, gameDisplay, width, color):
        for p_n in range(-1, len(self.points) - 1):
            pygame.draw.line(gameDisplay, color,
                             self.points[p_n].int_pair(),
                             self.points[p_n + 1].int_pair(), 
                             width
            )

    def __get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        
        for i in range(count):
            res.append(self.__get_point(base_points, i * alpha))

        return res
            
    def __get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1

        if deg == 0:
            return points[0]

        return points[deg] * alpha + self.__get_point(points, alpha, deg - 1) * (1 - alpha)


if __name__ == "__main__":
    window = PyGameCanvas()
    window.run()
