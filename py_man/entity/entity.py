from random import randint

import pygame
from pygame.math import Vector2

from py_man.utils.enums.direction.joypad.joypad import JoyPad
from py_man.utils.enums.display.display import Display


class Entity(object):
    def __init__(self, node):
        self.speed = None
        self.position = None
        self.node = node
        self.inception_node = None
        self.set_inception_node(node)
        self.target = None
        self.display = Display()
        self.visibility = True
        self.sprite = None
        self.color = "white"
        self.radius = 10
        self.collision_radius = 5
        self.set_speed(100)
        self.name = None
        self.joypad = JoyPad()
        self.directions = {
            self.joypad.UP: Vector2(0, -1),
            self.joypad.RIGHT: Vector2(1, 0),
            self.joypad.DOWN: Vector2(0, 1),
            self.joypad.LEFT: Vector2(-1, 0),
            self.joypad.STOP: Vector2(),
        }
        self.direction = self.joypad.STOP
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

    def set_entity_between_nodes(self, direction):
        target_node = self.node.neighbors[direction]
        if target_node:
            self.target = target_node
            self.position = (self.node.position + target_node.position) / 2

    def render(self, screen):
        adjusted_position = Vector2(self.display.TILE_WIDTH, self.display.TILE_HEIGHT) / 2
        if self.visibility:
            position = self.position - adjusted_position
            if self.sprite is not None:
                screen.blit(self.sprite, (position.x, position.y))
            else:
                position = position.int()
                pygame.draw.circle(screen, self.color, position, self.radius)

    def set_speed(self, speed):
        self.speed = speed * self.display.TILE_WIDTH / 16

    def valid_direction(self, direction):
        return (
            direction != self.joypad.STOP
            and self.name in self.node.access[direction]
            and self.node.neighbors[direction] is not None
        )

    def valid_directions(self):
        valid_directions = [
            key
            for key in [
                self.joypad.UP,
                self.joypad.DOWN,
                self.joypad.LEFT,
                self.joypad.RIGHT,
            ]
            if self.valid_direction(key) and key != self.direction * -1
        ]
        return valid_directions or [self.direction * -1]

    def reverse_direction(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def opposite_direction(self, direction):
        return direction is not self.joypad.STOP and direction == -self.direction

    def random_direction(self, directions):
        return self and directions[randint(0, len(directions) - 1)]

    def goal_direction(self, directions):
        distances = [
            (
                self.node.position
                + self.directions[d] * self.display.TILE_WIDTH
                - self.goal
            ).magnitude_squared()
            for d in directions
        ]
        return min(directions, key=lambda d: distances[directions.index(d)])

    def get_new_target(self, direction):
        return (
            self.node.neighbors.get(direction, self.node)
            if self.valid_direction(direction)
            else self.node
        )

    def overshoot_target(self):
        if self.target is None:
            return False
        distance_between_the_current_node_and_py_man = (
            self.target.position - self.node.position
        ).magnitude_squared()
        distance_between_the_target_node_and_py_man = (
            self.position - self.node.position
        ).magnitude_squared()
        return (
            distance_between_the_target_node_and_py_man
            >= distance_between_the_current_node_and_py_man
        )

    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt
        if not self.overshoot_target():
            return
        self.node = self.target
        directions = self.valid_directions()
        direction = self.direction_method(directions)
        if not self.disable_portal and self.node.neighbors[JoyPad().PORTAL]:
            self.node = self.node.neighbors[JoyPad().PORTAL]
        self.target = self.get_new_target(direction)
        if self.target is self.node:
            self.target = self.get_new_target(self.direction)
        else:
            self.direction = direction
        self.set_position()

    def reset(self):
        self.set_inception_node(self.inception_node)
        self.visibility = True
        self.direction = self.joypad.STOP
        self.speed = 100
