import pygame
from pygame.locals import K_UP, K_RIGHT, K_DOWN, K_LEFT

from py_man.entity.entity import Entity
from py_man.utils.enums.display.character.character import Character
from py_man.utils.enums.direction.joypad.joypad import JoyPad
from py_man.assets.sprites.sprites import PyManSprites


class PyMan(Entity):
    def __init__(self, node):
        super().__init__(node)
        self.name = Character().PY_MAN
        self.color = "yellow"
        self.joypad = JoyPad()
        self.direction = self.joypad.LEFT
        self.set_entity_between_nodes(self.joypad.LEFT)
        self.alive = True
        self.sprites = PyManSprites(self)

    def valid_key(self):
        key_pressed = pygame.key.get_pressed()
        key_map = {
            K_UP: self.joypad.UP,
            K_RIGHT: self.joypad.RIGHT,
            K_DOWN: self.joypad.DOWN,
            K_LEFT: self.joypad.LEFT,
        }
        for key, value in key_map.items():
            if key_pressed[key]:
                return value
        return self and self.joypad.STOP

    def collision_type(self, other):
        distance = self.position - other.position
        radius_sum = self.collision_radius + other.collision_radius
        if distance.length() > radius_sum:
            return False
        return distance.dot(distance) <= radius_sum**2

    def devour_pellet(self, pelle_list):
        for pellet in pelle_list:
            if self.collision_type(pellet):
                return pellet
        return None

    def collide_with_ghost(self, ghost):
        return self.collision_type(ghost)

    def died(self):
        self.alive = False
        self.direction = self.joypad.STOP

    def update(self, dt):
        self.sprites.update(dt)
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.valid_key()
        if self.overshoot_target():
            self.node = self.target
            if (portal := self.node.neighbors[self.joypad.PORTAL]) is not None:
                self.node = portal
            if (target := self.get_new_target(direction)) is not self.node:
                self.direction = direction
            else:
                target = self.get_new_target(self.direction)
                if target is self.node:
                    self.direction = self.joypad.STOP
            self.target = target
            self.set_position()
        else:
            if self.opposite_direction(direction):
                self.reverse_direction()

    def reset(self):
        Entity.reset(self)
        self.direction = self.joypad.LEFT
        self.set_entity_between_nodes(self.direction)
        self.alive = True
        self.sprite = self.sprites.return_initial_sprite()
        self.sprites.reset()
