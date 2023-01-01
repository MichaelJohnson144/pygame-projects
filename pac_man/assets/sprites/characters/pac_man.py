import pygame
from pygame.locals import K_UP, K_RIGHT, K_DOWN, K_LEFT

from pac_man.assets.sprites.sprites import PacManSprites
from pac_man.entity.entity import Entity
from pac_man.utils.enums.direction.joypad.joypad import Joypad
from pac_man.utils.enums.display.character.character import Character


class PacMan(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = Character().PAC_MAN
        self.color = "yellow"
        self.direction = Joypad().LEFT
        self.set_entity_between_nodes(Joypad().LEFT)
        self.alive = True
        self.sprites = PacManSprites(self)

    def valid_key(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return Joypad().UP
        if key_pressed[K_RIGHT]:
            return Joypad().RIGHT
        if key_pressed[K_DOWN]:
            return Joypad().DOWN
        if key_pressed[K_LEFT]:
            return Joypad().LEFT
        return self and Joypad().STOP

    def collision_type(self, other):
        distance = self.position - other.position
        distance_squared = distance.magnitude_squared()
        radius_squared = (self.collision_radius + other.collision_radius) ** 2
        if distance_squared <= radius_squared:
            return True
        return False

    def devour_pellet(self, pelle_list):
        for pellet in pelle_list:
            if self.collision_type(pellet):
                return pellet
        return None

    def collide_with_ghost(self, ghost):
        return self.collision_type(ghost)

    def died(self):
        self.alive = False
        self.direction = Joypad().STOP

    def update(self, dt):
        self.sprites.update(dt)
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.valid_key()
        if self.overshoot_target():
            self.node = self.target
            if self.node.neighbors[Joypad().PORTAL] is not None:
                self.node = self.node.neighbors[Joypad().PORTAL]
            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)
            if self.target is self.node:
                self.direction = Joypad().STOP
            self.set_position()
        else:
            if self.opposite_direction(direction):
                self.reverse_direction()

    def reset(self):
        Entity.reset(self)
        self.direction = Joypad().LEFT
        self.set_entity_between_nodes(Joypad().LEFT)
        self.alive = True
        self.sprite = self.sprites.return_initial_sprite()
        self.sprites.reset()
