import numpy as np
import pygame

from pac_man.utils.enums.display.character.character import Character
from pac_man.utils.enums.display.display import Display
from pac_man.vector.vector import Vector2


class Pellet(object):
    def __init__(self, i, j):
        self.name = Character().PELLET
        self.visibility = True
        self.position = Vector2(j * Display().TILE_WIDTH, i * Display().TILE_HEIGHT)
        self.pellet_radius = int(2 * Display().TILE_WIDTH / 16)
        self.collision_radius = 2 * Display().TILE_WIDTH / 16
        self.points = 10

    def render(self, screen):
        if self.visibility:
            adjusted_pellet_position = (
                Vector2(Display().TILE_WIDTH, Display().TILE_HEIGHT) / 2
            )
            pellet_position = self.position + adjusted_pellet_position
            pygame.draw.circle(
                screen, "#DEA185", pellet_position.int(), self.pellet_radius
            )


class PowerPellet(Pellet):
    def __init__(self, i, j):
        Pellet.__init__(self, i, j)
        self.name = Character().POWER_PELLET
        self.pellet_radius = int(8 * Display().TILE_WIDTH / 16)
        self.points = 50
        self.timer = 0
        self.flash_time = 0.2

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flash_time:
            self.visibility = not self.visibility
            self.timer = 0


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
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if data[i][j] in [".", "+"]:
                    self.pellet_array.append(Pellet(i, j))
                elif data[i][j] in ["P", "p"]:
                    power_pellet = PowerPellet(i, j)
                    self.pellet_array.append(power_pellet)
                    self.power_pellet_array.append(power_pellet)

    def render(self, screen):
        for pellet in self.pellet_array:
            pellet.render(screen)

    def empty(self):
        if len(self.pellet_array) == 0:
            return True
        return False

    def update(self, dt):
        for power_pellet in self.power_pellet_array:
            power_pellet.update(dt)
