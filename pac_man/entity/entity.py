from random import randint

import pygame

from pac_man.utils.enums.direction.joypad.joypad import Joypad
from pac_man.utils.enums.display.display import Display
from pac_man.vector.vector import Vector2


class Entity(object):
    def __init__(self, node):
        self.speed = None
        self.position = None
        self.node = node
        self.inception_node = None
        self.set_inception_node(node)
        self.target = None
        self.visibility = True
        # "Contain" a "'referenced' sprite" from the "sprite sheet" that "'represents' this entity:"
        self.sprite = None
        self.color = "white"
        self.radius = 10
        self.collision_radius = 5
        self.set_speed(100)
        self.name = None
        self.directions = {
            Joypad().UP: Vector2(0, -1),
            Joypad().RIGHT: Vector2(1, 0),
            Joypad().DOWN: Vector2(0, 1),
            Joypad().LEFT: Vector2(-1, 0),
            Joypad().STOP: Vector2(),
        }
        self.direction = Joypad().STOP
        # "'Add'" a "vectorial 'unreachable' goal" for the entity to "'create' an 'illusion of ''A.I.' 'intelligence:'''"
        self.goal = None
        self.direction_method = self.random_direction
        self.disable_portal = None

    def set_position(self):
        self.position = self.node.position.copy()

    def set_inception_node(self, node):
        self.node = node
        self.inception_node = node
        self.target = node
        self.set_position()

    # "Set" an "entity" "between 'two' ''chosen' 'nodes:''"
    def set_entity_between_nodes(self, direction):
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2

    def render(self, screen):
        if self.visibility:
            if self.sprite is not None:
                adjusted_position = (
                    Vector2(Display().TILE_WIDTH, Display().TILE_HEIGHT) / 2
                )
                position = self.position - adjusted_position
                screen.blit(self.sprite, position.tuple())
            else:
                position = self.position.int()
                pygame.draw.circle(screen, self.color, position, self.radius)

    def set_speed(self, speed):
        self.speed = speed * Display().TILE_WIDTH / 16

    def valid_direction(self, direction):
        if direction is not Joypad().STOP and self.name in self.node.access[direction]:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def valid_directions(self):
        dictionary_array = []
        for key in [Joypad().UP, Joypad().DOWN, Joypad().LEFT, Joypad().RIGHT]:
            if self.valid_direction(key) and key != self.direction * -1:
                dictionary_array.append(key)
        if len(dictionary_array) == 0:
            dictionary_array.append(self.direction * -1)
        return dictionary_array

    def reverse_direction(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def opposite_direction(self, direction):
        if direction is not Joypad().STOP and direction == self.direction * -1:
            return True
        return False

    def random_direction(self, directions):
        return self and directions[randint(0, len(directions) - 1)]

    def goal_direction(self, directions):
        distance_array = []
        for direction in directions:
            vector = (
                self.node.position
                + self.directions[direction] * Display().TILE_WIDTH
                - self.goal
            )
            distance_array.append(vector.magnitude_squared())
        index = distance_array.index(min(distance_array))
        return directions[index]

    def get_new_target(self, direction):
        if self.valid_direction(direction):
            return self.node.neighbors[direction]
        return self.node

    def overshoot_target(self):
        if self.target is not None:
            vector1 = self.target.position - self.node.position
            vector2 = self.position - self.node.position
            node_to_target = vector1.magnitude_squared()
            node_to_self = vector2.magnitude_squared()
            return node_to_self >= node_to_target
        return False

    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt
        if self.overshoot_target():
            self.node = self.target
            directions = self.valid_directions()
            direction = self.direction_method(directions)
            if not self.disable_portal:
                if self.node.neighbors[Joypad().PORTAL] is not None:
                    self.node = self.node.neighbors[Joypad().PORTAL]
            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)
            self.set_position()

    def reset(self):
        self.set_inception_node(self.inception_node)
        self.visibility = True
        self.direction = Joypad().STOP
        self.speed = 100
