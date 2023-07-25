from py_man.utils.enums.direction.joypad.joypad import JoyPad


class MazeBase(object):
    def __init__(self):
        self.portal_dictionary = {}
        self.legend_layout_offset = (0, 0)
        self.joypad = JoyPad()
        self.initial_node_right_connection = None
        self.initial_node_left_connection = None
        self.ghost_denied_node = {
            self.joypad.UP: (),
            self.joypad.RIGHT: (),
            self.joypad.DOWN: (),
            self.joypad.LEFT: (),
        }

    def connect_portals(self, nodes):
        for node_pair in self.portal_dictionary.values():
            if isinstance(node_pair, tuple) and len(node_pair) == 2:
                nodes.connect_portals(*node_pair)

    def link_vertically(self, nodes):
        key = nodes.generate_spawn_point_layout(*self.legend_layout_offset)
        for direction, connection in [
            (self.joypad.RIGHT, self.initial_node_right_connection),
            (self.joypad.LEFT, self.initial_node_left_connection),
        ]:
            nodes.link_spawn_point_layout(key, connection, direction)

    def add_offset(self, x, y):
        return x + self.legend_layout_offset[0], y + self.legend_layout_offset[1]

    def block_access(self, ghosts, nodes):
        denied_nodes = [
            self.add_offset(2, 3) + (direction, ghosts)
            for direction in [self.joypad.RIGHT, self.joypad.LEFT]
        ]
        ghost_denied_nodes = [
            (value + (direction, ghosts))
            for direction, values in self.ghost_denied_node.items()
            for value in values
        ]
        all_denied_nodes = denied_nodes + ghost_denied_nodes
        for values in all_denied_nodes:
            nodes.block_direction_for_entities(*values)


class MazeA(MazeBase):
    def __init__(self):
        super().__init__()
        self.name = "maze_a"
        self.portal_dictionary = {0: ((0, 17), (27, 17))}
        self.legend_layout_offset = (11.5, 14)
        self.initial_node_right_connection = (15, 14)
        self.initial_node_left_connection = (12, 14)
        self.py_man_inception_node = (15, 26)
        self.fruit_inception_node = (9, 20)
        self.joypad = JoyPad()
        self.ghost_denied_node = {
            self.joypad.UP: ((12, 14), (15, 14), (12, 26), (15, 26)),
            self.joypad.RIGHT: (self.add_offset(2, 3),),
            self.joypad.LEFT: (self.add_offset(2, 3),),
        }


class MazeB(MazeBase):
    def __init__(self):
        super().__init__()
        self.name = "maze_b"
        self.portal_dictionary = {0: ((0, 4), (27, 4)), 1: ((0, 26), (27, 26))}
        self.legend_layout_offset = (11.5, 14)
        self.initial_node_left_connection = (9, 14)
        self.initial_node_right_connection = (18, 14)
        self.py_man_inception_node = (16, 26)
        self.fruit_inception_node = (11, 20)
        self.joypad = JoyPad()
        self.ghost_denied_node = {
            self.joypad.UP: ((9, 14), (18, 14), (11, 23), (16, 23)),
            self.joypad.RIGHT: (self.add_offset(2, 3),),
            self.joypad.LEFT: (self.add_offset(2, 3),),
        }


class MazeData(object):
    def __init__(self):
        self.maze_dictionary = {0: MazeA, 1: MazeB}
        self.maze_object = None

    def load(self, level):
        maze_count = len(self.maze_dictionary)
        maze_index = level % maze_count
        self.maze_object = self.maze_dictionary[maze_index]()
