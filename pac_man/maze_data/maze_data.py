from pac_man.utils.enums.direction.joypad.joypad import Joypad


# This class will "'generalize' ''every' 'maze file'' that's 'referenced' in 'rum.py:'"
class MazeBase(object):
    def __init__(self):
        self.inception_node_right_connection = None
        self.inception_node_left_connection = None
        self.portal_dictionary = {}
        self.maze_legend_offset = (0, 0)
        self.ghost_denied_node = {
            Joypad().UP: (),
            Joypad().DOWN: (),
            Joypad().LEFT: (),
            Joypad().RIGHT: (),
        }

    def setup_portals(self, nodes):
        for pair in list(self.portal_dictionary.values()):
            nodes.setup_portals(*pair)

    def connect_maze_legend(self, nodes):
        key = nodes.create_maze_legend(*self.maze_legend_offset)
        nodes.connect_maze_legend(key, self.inception_node_left_connection, Joypad().LEFT)
        nodes.connect_maze_legend(
            key, self.inception_node_right_connection, Joypad().RIGHT
        )

    def add_offset(self, x, y):
        return x + self.maze_legend_offset[0], y + self.maze_legend_offset[1]

    def deny_ghosts_access(self, ghosts, nodes):
        nodes.denied_list(*(self.add_offset(2, 3) + (Joypad().LEFT, ghosts)))
        nodes.denied_list(*(self.add_offset(2, 3) + (Joypad().RIGHT, ghosts)))

        for direction in list(self.ghost_denied_node.keys()):
            for values in self.ghost_denied_node[direction]:
                nodes.denied_list(*(values + (direction, ghosts)))


class MazeA(MazeBase):
    def __init__(self):
        MazeBase.__init__(self)
        self.name = "maze_a"
        self.portal_dictionary = {0: ((0, 17), (27, 17))}
        self.maze_legend_offset = (11.5, 14)
        self.inception_node_left_connection = (12, 14)
        self.inception_node_right_connection = (15, 14)
        self.pac_man_inception_node = (15, 26)
        self.fruit_inception_node = (9, 20)
        self.ghost_denied_node = {
            Joypad().UP: ((12, 14), (15, 14), (12, 26), (15, 26)),
            Joypad().LEFT: (self.add_offset(2, 3),),
            Joypad().RIGHT: (self.add_offset(2, 3),),
        }


class MazeB(MazeBase):
    def __init__(self):
        MazeBase.__init__(self)
        self.name = "maze_b"
        self.portal_dictionary = {0: ((0, 4), (27, 4)), 1: ((0, 26), (27, 26))}
        self.maze_legend_offset = (11.5, 14)
        self.inception_node_left_connection = (9, 14)
        self.inception_node_right_connection = (18, 14)
        self.pac_man_inception_node = (16, 26)
        self.fruit_inception_node = (11, 20)
        self.ghost_denied_node = {
            Joypad().UP: ((9, 14), (18, 14), (11, 23), (16, 23)),
            Joypad().LEFT: (self.add_offset(2, 3),),
            Joypad().RIGHT: (self.add_offset(2, 3),),
        }


class MazeData(object):
    def __init__(self):
        self.maze_object = None
        self.maze_dictionary = {0: MazeA, 1: MazeB}

    # "'Load' the 'maze 'levels'' upon request:"
    def load(self, level):
        self.maze_object = self.maze_dictionary[level % len(self.maze_dictionary)]()
