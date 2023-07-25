import numpy as np
import pygame
from pygame import Vector2

from py_man.utils.enums.direction.joypad.joypad import JoyPad
from py_man.utils.enums.display.character.character import Character
from py_man.utils.enums.display.display import Display


class Node(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.joypad = JoyPad()
        self.name = Character()
        self.neighbors = {
            self.joypad.UP: None,
            self.joypad.RIGHT: None,
            self.joypad.DOWN: None,
            self.joypad.LEFT: None,
            self.joypad.PORTAL: None,
        }
        access_list = [
            self.name.PY_MAN,
            self.name.BLINKY,
            self.name.PINKY,
            self.name.INKY,
            self.name.CLYDE,
            self.name.FRUIT,
        ]
        self.access = {direction: access_list.copy() for direction in self.neighbors}

    def block_direction(self, direction, entity):
        if entity.name in self.access[direction]:
            self.access[direction].remove(entity.name)

    def allow_direction(self, direction, entity):
        if entity.name not in self.access[direction]:
            self.access[direction].append(entity.name)

    def render(self, screen):
        for neighbor in filter(None, self.neighbors.values()):
            inception_line = (int(self.position.x), int(self.position.y))
            final_line = (int(neighbor.position.x), int(neighbor.position.y))
            pygame.draw.line(screen, "white", inception_line, final_line, 4)
            pygame.draw.circle(screen, "red", inception_line, 12)


class NodeGroup(object):
    def __init__(self, level, spawn_point_key=None):
        self.level = level
        self.display = Display()
        self.node_symbols_array = ["+", "P", "n"]
        self.node_dictionary = {}
        self.joypad = JoyPad()
        self.path_symbols_array = [".", "-", "|", "p"]
        data = self.load(level)
        self.generate(data)
        self.link_horizontally(data)
        self.link_vertically(data)
        self.spawn_point_key = spawn_point_key

    @staticmethod
    def load(maze_text_file):
        return np.loadtxt(maze_text_file, dtype="<U1")

    def calculate_node_key(self, x, y):
        return x * self.display.TILE_WIDTH, y * self.display.TILE_HEIGHT

    def generate(self, data, x_offset=0, y_offset=0):
        node_indices = np.where(np.isin(data, self.node_symbols_array))
        for i, j in zip(node_indices[1], node_indices[0]):
            x, y = self.calculate_node_key(i + x_offset, j + y_offset)
            self.node_dictionary[(x, y)] = Node(x, y)

    def link_horizontally(self, data, x_offset=0, y_offset=0):
        for j, row in enumerate(data):
            spawn_point_key = None
            for i, value in enumerate(row):
                if value in self.node_symbols_array:
                    key = self.calculate_node_key(i + x_offset, j + y_offset)
                    if spawn_point_key:
                        self.node_dictionary[spawn_point_key].neighbors[
                            self.joypad.RIGHT
                        ] = self.node_dictionary[key]
                        self.node_dictionary[key].neighbors[self.joypad.LEFT] = (
                            self.node_dictionary[spawn_point_key]
                        )
                    spawn_point_key = key
                elif value not in self.path_symbols_array:
                    spawn_point_key = None

    def link_vertically(self, data, x_offset=0, y_offset=0):
        data_type = data.transpose()
        for i, row in enumerate(data_type):
            spawn_point_key = None
            for j, value in enumerate(row):
                if value in self.node_symbols_array:
                    key = self.calculate_node_key(i + x_offset, j + y_offset)
                    if spawn_point_key:
                        self.node_dictionary[spawn_point_key].neighbors[
                            self.joypad.DOWN
                        ] = self.node_dictionary[key]
                        self.node_dictionary[key].neighbors[self.joypad.UP] = (
                            self.node_dictionary[spawn_point_key]
                        )
                    spawn_point_key = key
                elif value not in self.path_symbols_array:
                    spawn_point_key = None

    def get_inception_node(self):
        nodes = list(self.node_dictionary.values())
        return nodes[0]

    def connect_portals(self, first_portal, second_portal):
        spawn_point_key, neighbouring_node_key = [
            self.calculate_node_key(*portal) for portal in (first_portal, second_portal)
        ]
        self.node_dictionary[spawn_point_key].neighbors[self.joypad.PORTAL] = (
            self.node_dictionary[neighbouring_node_key]
        )
        self.node_dictionary[neighbouring_node_key].neighbors[self.joypad.PORTAL] = (
            self.node_dictionary[spawn_point_key]
        )

    def generate_spawn_point_layout(self, x_offset, y_offset):
        spawn_point_node_array = np.array(
            [
                ["X", "X", "+", "X", "X"],
                ["X", "X", ".", "X", "X"],
                ["+", "X", ".", "X", "+"],
                ["+", ".", "+", ".", "+"],
                ["+", "X", "X", "X", "+"],
            ]
        )
        self.generate(spawn_point_node_array, x_offset, y_offset)
        self.link_horizontally(spawn_point_node_array, x_offset, y_offset)
        self.link_vertically(spawn_point_node_array, x_offset, y_offset)
        self.spawn_point_key = self.calculate_node_key(x_offset + 2, y_offset)
        return self.spawn_point_key

    def link_spawn_point_layout(self, spawn_point_key, neighbouring_node_key, direction):
        self.node_dictionary[spawn_point_key].neighbors[direction] = (
            self.retrieve_from_tile_coordinates(*neighbouring_node_key)
        )
        self.node_dictionary[self.calculate_node_key(*neighbouring_node_key)].neighbors[
            direction * -1
        ] = self.node_dictionary[spawn_point_key]

    def retrieve_from_pixel_coordinates(self, x_pixel, y_pixel):
        return self.node_dictionary.get((x_pixel, y_pixel), None)

    def retrieve_from_tile_coordinates(self, i, j):
        return self.node_dictionary.get(self.calculate_node_key(i, j), None)

    def manage_accessible_directions(self, i, j, direction, entity, action):
        node = self.retrieve_from_tile_coordinates(i, j)
        if node is not None:
            if action == "allow":
                node.allow_direction(direction, entity)
            elif action == "block":
                node.block_direction(direction, entity)

    def modify_access_for_entities(self, i, j, direction, entities, action):
        for entity in entities:
            self.manage_accessible_directions(i, j, direction, entity, action)

    def block_direction(self, i, j, direction, entity):
        self.manage_accessible_directions(i, j, direction, entity, "block")

    def block_direction_for_entities(self, i, j, direction, entities):
        self.modify_access_for_entities(i, j, direction, entities, "block")

    def block_spawn_point_movements(self, entity):
        self.manage_accessible_directions(
            self.spawn_point_key[0],
            self.spawn_point_key[1],
            self.joypad.DOWN,
            entity,
            "block",
        )

    def block_spawn_point_movements_for_entities(self, entities):
        self.modify_access_for_entities(
            self.spawn_point_key[0],
            self.spawn_point_key[1],
            self.joypad.DOWN,
            entities,
            "block",
        )

    def allow_direction(self, i, j, direction, entity):
        self.manage_accessible_directions(i, j, direction, entity, "allow")

    def allow_direction_for_entities(self, i, j, direction, entities):
        self.modify_access_for_entities(i, j, direction, entities, "allow")

    def allow_spawn_point_movements(self, entity):
        self.manage_accessible_directions(
            self.spawn_point_key[0],
            self.spawn_point_key[1],
            self.joypad.DOWN,
            entity,
            "allow",
        )

    def allow_spawn_point_movements_for_entities(self, entities):
        self.modify_access_for_entities(
            self.spawn_point_key[0],
            self.spawn_point_key[1],
            self.joypad.DOWN,
            entities,
            "allow",
        )

    def render(self, screen):
        for node in self.node_dictionary.values():
            node.render(screen)
