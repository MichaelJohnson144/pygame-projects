import numpy as np
import pygame

from pac_man.utils.enums.direction.joypad.joypad import Joypad
from pac_man.utils.enums.display.character.character import Character
from pac_man.utils.enums.display.display import Display
from pac_man.vector.vector import Vector2


class Node(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {
            Joypad().UP: None,
            Joypad().DOWN: None,
            Joypad().LEFT: None,
            Joypad().RIGHT: None,
            Joypad().PORTAL: None,
        }
        self.access = {
            Joypad().UP: [
                Character().PAC_MAN,
                Character().BLINKY,
                Character().PINKY,
                Character().INKY,
                Character().CLYDE,
                Character().FRUIT,
            ],
            Joypad().RIGHT: [
                Character().PAC_MAN,
                Character().BLINKY,
                Character().PINKY,
                Character().INKY,
                Character().CLYDE,
                Character().FRUIT,
            ],
            Joypad().DOWN: [
                Character().PAC_MAN,
                Character().BLINKY,
                Character().PINKY,
                Character().INKY,
                Character().CLYDE,
                Character().FRUIT,
            ],
            Joypad().LEFT: [
                Character().PAC_MAN,
                Character().BLINKY,
                Character().PINKY,
                Character().INKY,
                Character().CLYDE,
                Character().FRUIT,
            ],
        }

    def deny_access(self, direction, entity):
        if entity.name in self.access[direction]:
            self.access[direction].remove(entity.name)

    def grant_access(self, direction, entity):
        if entity.name not in self.access[direction]:
            self.access[direction].append(entity.name)

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                inception_line = self.position.tuple()
                final_line = self.neighbors[n].position.tuple()
                pygame.draw.line(screen, "white", inception_line, final_line, 4)
                pygame.draw.circle(screen, "red", self.position.int(), 12)


# This class with "group" all the nodes together:
class NodeGroup(object):
    def __init__(self, level, legend_key=None):
        self.level = level
        # "Create" a "dictionary" that'll "contain" and "reference" "'all' of the program's 'nodes:'"
        self.node_dictionary = {}
        # "Create" a "array" that'll "contain" and "reference" "'all' of the program's 'respective 'node' symbols:'"
        self.node_symbols_array = ["+", "P", "n"]
        # "Create" a "array" that'll "contain" and "reference" "'all' of the program's 'respective 'path' symbols:'"
        self.path_symbols_array = [".", "-", "|", "p"]
        data = self.load(level)
        self.create_node_dictionary(data)
        self.connect_nodes_horizontally(data)
        self.connect_nodes_vertically(data)
        # This key will "return" the "top node" of the "maze legend" so that it can be "'added' with it" because the offset
        # describes "'where to position' the 'top left corner' of the 'node array:'"
        self.legend_key = legend_key

    # "Read" the "maze's text data" and return a "'2D' array:"
    def load(self, maze_text_file):
        return self and np.loadtxt(maze_text_file, dtype="<U1")

    def construct_legend_key(self, x, y):
        return self and x * Display().TILE_WIDTH, y * Display().TILE_HEIGHT

    def create_node_dictionary(self, data, x_offset=0, y_offset=0):
        for j in list(range(data.shape[0])):
            for i in list(range(data.shape[1])):
                if data[j][i] in self.node_symbols_array:
                    x, y = self.construct_legend_key(i + x_offset, j + y_offset)
                    self.node_dictionary[(x, y)] = Node(x, y)

    # "Connect" the "'nodes' ''horizontally' together with each other:'"
    def connect_nodes_horizontally(self, data, x_offset=0, y_offset=0):
        for j in list(range(data.shape[0])):
            first_key = None
            for i in list(range(data.shape[1])):
                if data[j][i] in self.node_symbols_array:
                    if first_key is None:
                        first_key = self.construct_legend_key(i + x_offset, j + y_offset)
                    else:
                        second_key = self.construct_legend_key(i + x_offset, j + y_offset)
                        self.node_dictionary[first_key].neighbors[
                            Joypad().RIGHT
                        ] = self.node_dictionary[second_key]
                        self.node_dictionary[second_key].neighbors[
                            Joypad().LEFT
                        ] = self.node_dictionary[first_key]
                        first_key = second_key
                elif data[j][i] not in self.path_symbols_array:
                    first_key = None

    # "Connect" the "'nodes' ''vertically' together with each other:'"
    def connect_nodes_vertically(self, data, x_offset=0, y_offset=0):
        data_type = data.transpose()
        for i in list(range(data_type.shape[0])):
            first_key = None
            for j in list(range(data_type.shape[1])):
                if data_type[i][j] in self.node_symbols_array:
                    if first_key is None:
                        first_key = self.construct_legend_key(i + x_offset, j + y_offset)
                    else:
                        second_key = self.construct_legend_key(i + x_offset, j + y_offset)
                        self.node_dictionary[first_key].neighbors[
                            Joypad().DOWN
                        ] = self.node_dictionary[second_key]
                        self.node_dictionary[second_key].neighbors[
                            Joypad().UP
                        ] = self.node_dictionary[first_key]
                        first_key = second_key
                elif data_type[i][j] not in self.path_symbols_array:
                    first_key = None

    # "Pre-define" Pac-Man's "'inception' node:"
    def get_inception_node(self):
        nodes = list(self.node_dictionary.values())
        return nodes[0]

    # "Pre-define" the "pair of 'portals:'"
    def setup_portals(self, first_portal, second_portal):
        first_key = self.construct_legend_key(*first_portal)
        second_key = self.construct_legend_key(*second_portal)
        if (
            first_key in self.node_dictionary.keys()
            and second_key in self.node_dictionary.keys()
        ):
            self.node_dictionary[first_key].neighbors[
                Joypad().PORTAL
            ] = self.node_dictionary[second_key]
            self.node_dictionary[second_key].neighbors[
                Joypad().PORTAL
            ] = self.node_dictionary[first_key]

    # "Pre-define" the "maze text files' 'legend,'" with "X" denoting the maze's "paths," and "+" denoting the maze's "nodes,"
    # and subsequently finally "'position' the nodes in 'reference' to the 'respective offsets' correctly:"
    def create_maze_legend(self, x_offset, y_offset):
        node_legend_array = np.array(
            [
                ["X", "X", "+", "X", "X"],
                ["X", "X", ".", "X", "X"],
                ["+", "X", ".", "X", "+"],
                ["+", ".", "+", ".", "+"],
                ["+", "X", "X", "X", "+"],
            ]
        )
        self.create_node_dictionary(node_legend_array, x_offset, y_offset)
        self.connect_nodes_horizontally(node_legend_array, x_offset, y_offset)
        self.connect_nodes_vertically(node_legend_array, x_offset, y_offset)
        self.legend_key = self.construct_legend_key(x_offset + 2, y_offset)
        return self.legend_key

    def connect_maze_legend(self, legend_key, second_key, direction):
        key = self.construct_legend_key(*second_key)
        self.node_dictionary[legend_key].neighbors[direction] = self.node_dictionary[key]
        self.node_dictionary[key].neighbors[direction * -1] = self.node_dictionary[
            legend_key
        ]

    def get_from_pixels(self, x_pixel, y_pixel):
        if (x_pixel, y_pixel) in self.node_dictionary.keys():
            return self.node_dictionary[(x_pixel, y_pixel)]
        return None

    def get_from_tiles(self, i, j):
        x, y = self.construct_legend_key(i, j)
        if (x, y) in self.node_dictionary.keys():
            return self.node_dictionary[(x, y)]
        return None

    def deny_access(self, i, j, direction, entity):
        node = self.get_from_tiles(i, j)
        if node is not None:
            node.deny_access(direction, entity)

    def denied_list(self, i, j, direction, entities):
        for entity in entities:
            self.deny_access(i, j, direction, entity)

    def deny_home_access(self, entity):
        self.node_dictionary[self.legend_key].deny_access(Joypad().DOWN, entity)

    def denied_home_list(self, entities):
        for entity in entities:
            self.deny_home_access(entity)

    def grant_access(self, i, j, direction, entity):
        node = self.get_from_tiles(i, j)
        if node is not None:
            node.grant_access(direction, entity)

    def permitted_listed(self, i, j, direction, entities):
        for entity in entities:
            self.grant_access(i, j, direction, entity)

    def grant_home_access(self, entity):
        self.node_dictionary[self.legend_key].grant_access(Joypad().DOWN, entity)

    def permitted_home_list(self, entities):
        for entity in entities:
            self.grant_home_access(entity)

    def render(self, screen):
        for node in self.node_dictionary.values():
            node.render(screen)
