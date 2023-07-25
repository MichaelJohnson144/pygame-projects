import numpy as np
import pygame
from pygame import Vector2

from py_man.utils.enums.display.character.character import Character
from py_man.utils.enums.display.display import Display


class Pellet(object):
    def __init__(self, i, j):
        self.name = Character().PELLET
        self.display = Display()
        self.visibility = True
        self.position = Vector2(j * self.display.TILE_WIDTH, i * self.display.TILE_HEIGHT)
        self.pellet_radius = int(2 * self.display.TILE_WIDTH / 16)
        self.collision_radius = 2 * self.display.TILE_WIDTH / 16
        self.points = 10

    def render(self, screen):
        if not self.visibility:
            return
        tile_size = Vector2(self.display.TILE_WIDTH, self.display.TILE_HEIGHT)
        adjusted_pellet_position = tile_size / 2
        pellet_position = self.position + adjusted_pellet_position
        pygame.draw.circle(
            screen, "#DEA185", tuple(int(x) for x in pellet_position), self.pellet_radius
        )


class PowerPellet(Pellet):
    def __init__(self, i, j):
        super().__init__(i, j)
        self.name = Character().POWER_PELLET
        self.pellet_radius = int(8 * Display().TILE_WIDTH / 16)
        self.points = 50
        self.timer = 0
        self.flash_time = 0.2

    def update(self, dt):
        self.timer += dt
        self.visibility = (self.timer // self.flash_time) % 2 == 0


class PelletGroup(object):
    def __init__(self, pellet_file):
        self.pellet_array = []
        self.power_pellet_array = []
        self.create(pellet_file)
        self.number_eaten = 0

    def load(self, maze_text_file):
        return self and np.loadtxt(maze_text_file, dtype="<U1")

    def create(self, pellet_file):
        data = self.load(pellet_file)
        for i, row in enumerate(data):
            for j, cell in enumerate(row):
                if cell in (".", "+"):
                    self.pellet_array.append(Pellet(i, j))
                elif cell.lower() == "p":
                    power_pellet = PowerPellet(i, j)
                    self.pellet_array.append(power_pellet)
                    self.power_pellet_array.append(power_pellet)

    def render(self, screen):
        for pellet in self.pellet_array:
            pellet.render(screen)

    def empty(self):
        return not self.pellet_array

    def update(self, dt):
        for power_pellet in self.power_pellet_array:
            power_pellet.update(dt)
