from pygame.math import Vector2

from py_man.assets.sprites.sprites import GhostSprites
from py_man.entity.entity import Entity
from py_man.state.states import StateController
from py_man.utils.enums.direction.joypad.joypad import JoyPad
from py_man.utils.enums.direction.state.ghost_state.ghost_state import GhostState
from py_man.utils.enums.display.character.character import Character
from py_man.utils.enums.display.display import Display


class Ghost(Entity):
    def __init__(self, node, py_man=None, blinky=None):
        super().__init__(node)
        self.spawn_point_node = None
        self.goal = Vector2()
        self.state_controller = StateController(self)
        self.ghost_state = GhostState()
        self.direction_method = self.goal_direction
        self.sprites = None
        self.points = 200
        self.py_man = py_man
        self.home_node = node
        self.name = Character().GHOST
        self.display = Display()
        self.blinky = blinky

    def set_spawn_point(self, node):
        self.spawn_point_node = node

    def set_spawn_goal(self):
        self.goal = self.spawn_point_node.position

    def initial_spawn_state(self):
        self.state_controller.spawn()
        if self.state_controller.current == self.ghost_state.SPAWN:
            self.set_speed(150)
            self.direction_method = self.goal_direction
            self.set_spawn_goal()

    def original_state(self):
        self.set_speed(100)
        self.direction_method = self.goal_direction
        self.home_node.block_direction(JoyPad().DOWN, self)

    def chase(self):
        self.goal = self.py_man.position

    def scatter(self):
        self.goal = Vector2()

    def frightened(self):
        self.state_controller.frightened()
        if self.state_controller.current == self.ghost_state.FRIGHTENED:
            self.set_speed(50)
            self.direction_method = self.random_direction

    def update(self, dt):
        self.sprites.update(dt)
        self.state_controller.update(dt)
        state_dictionary = {
            self.ghost_state.CHASE: self.chase,
            self.ghost_state.SCATTER: self.scatter,
        }
        current_state = self.state_controller.current
        if current_state in state_dictionary:
            state_dictionary[current_state]()
        Entity.update(self, dt)

    def reset(self):
        Entity.reset(self)
        self.points = 200
        self.direction_method = self.goal_direction
        self.state_controller.reset()


class Blinky(Ghost):
    def __init__(self, node, py_man=None, blinky=None):
        super().__init__(node, py_man, blinky)
        self.name = Character().BLINKY
        self.color = "red"
        self.sprites = GhostSprites(self)


class Pinky(Ghost):
    def __init__(self, node, py_man=None, blinky=None):
        super().__init__(node, py_man, blinky)
        self.name = Character().PINKY
        self.color = "#FFB8FF"
        self.sprites = GhostSprites(self)

    def chase(self):
        self.goal = (
            self.py_man.position
            + self.py_man.directions[self.py_man.direction] * self.display.TILE_WIDTH * 4
        )

    def scatter(self):
        self.goal = Vector2(self.display.TILE_WIDTH * self.display.N_COLS, 0)


class Inky(Ghost):
    def __init__(self, node, py_man=None, blinky=None):
        super().__init__(node, py_man, blinky)
        self.name = Character().INKY
        self.color = "aqua"
        self.sprites = GhostSprites(self)

    def chase(self):
        direction_to_py_man = self.py_man.position - self.blinky.position
        self.goal = self.blinky.position + direction_to_py_man * 2

    def scatter(self):
        self.goal = Vector2(
            self.display.TILE_WIDTH * self.display.N_COLS,
            self.display.TILE_HEIGHT * self.display.N_ROWS,
        )


class Clyde(Ghost):
    def __init__(self, node, py_man=None, blinky=None):
        super().__init__(node, py_man, blinky)
        self.name = Character().CLYDE
        self.color = "#FFB852"
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Vector2(0, self.display.TILE_HEIGHT * self.display.N_ROWS)

    def chase(self):
        distance = (self.py_man.position - self.position).magnitude_squared()
        (
            self.scatter()
            if distance <= (self.display.TILE_WIDTH * 8) ** 2
            else setattr(
                self,
                "goal",
                self.py_man.position
                + self.py_man.directions[self.py_man.direction]
                * self.display.TILE_WIDTH
                * 4,
            )
        )


class GhostGroup(object):
    def __init__(self, node, py_man):
        self.blinky = Blinky(node, py_man)
        self.pinky = Pinky(node, py_man)
        self.inky = Inky(node, py_man, self.blinky)
        self.clyde = Clyde(node, py_man)
        self.ghost_list = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        return iter(self.ghost_list)

    def set_spawn_point(self, node):
        for ghost in self:
            ghost.set_spawn_point(node)

    def render(self, screen):
        for ghost in self:
            ghost.render(screen)

    def show(self):
        for ghost in self:
            ghost.visibility = True

    def hide(self):
        for ghost in self:
            ghost.visibility = False

    def frightened(self):
        for ghost in self:
            ghost.frightened()
        self.reset_points()

    def update(self, dt):
        for ghost in self:
            ghost.update(dt)

    def update_points(self):
        for ghost in self:
            ghost.points *= 2

    def reset(self):
        for ghost in self:
            ghost.reset()

    def reset_points(self):
        for ghost in self:
            ghost.points = 200
