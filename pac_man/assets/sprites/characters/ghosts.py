from pac_man.assets.sprites.sprites import GhostSprites
from pac_man.entity.entity import Entity
from pac_man.state.states import StateController
from pac_man.utils.enums.direction.joypad.joypad import Joypad
from pac_man.utils.enums.direction.state.ghost_state.ghost_state import GhostState
from pac_man.utils.enums.display.character.character import Character
from pac_man.utils.enums.display.display import Display
from pac_man.vector.vector import Vector2


class Ghost(Entity):
    def __init__(self, node, pac_man=None, blinky=None):
        Entity.__init__(self, node)
        self.spawn_node = None
        self.goal = Vector2()
        self.mode = StateController(self)
        self.direction_method = self.goal_direction
        self.sprites = None
        self.points = 200
        self.pac_man = pac_man
        self.home_node = node
        self.name = Character().GHOST
        self.blinky = blinky

    def set_spawn_node(self, node):
        self.spawn_node = node

    def spawn(self):
        self.goal = self.spawn_node.position

    def initial_spawn_state(self):
        self.mode.set_spawn_state()
        if self.mode.current == GhostState().SPAWN:
            self.set_speed(150)
            self.direction_method = self.goal_direction
            self.spawn()

    def original_state(self):
        self.set_speed(100)
        self.direction_method = self.goal_direction
        self.home_node.deny_access(Joypad().DOWN, self)

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        self.goal = self.pac_man.position

    def initial_fright_state(self):
        self.mode.set_freight_state()
        if self.mode.current == GhostState().FRIGHTENED:
            self.set_speed(50)
            self.direction_method = self.random_direction

    def update(self, dt):
        self.sprites.update(dt)
        self.mode.update(dt)
        if self.mode.current is GhostState().SCATTER:
            self.scatter()
        elif self.mode.current is GhostState().CHASE:
            self.chase()
        Entity.update(self, dt)

    def reset(self):
        Entity.reset(self)
        self.points = 200
        self.direction_method = self.goal_direction


class Blinky(Ghost):
    def __init__(self, node, pac_man=None, blinky=None):
        Ghost.__init__(self, node, pac_man, blinky)
        self.name = Character().BLINKY
        self.color = "red"
        self.sprites = GhostSprites(self)


class Pinky(Ghost):
    def __init__(self, node, pac_man=None, blinky=None):
        Ghost.__init__(self, node, pac_man, blinky)
        self.name = Character().PINKY
        self.color = "#FFB8FF"
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Vector2(Display().TILE_WIDTH * Display().N_COLS, 0)

    def chase(self):
        self.goal = (
            self.pac_man.position
            + self.pac_man.directions[self.pac_man.direction] * Display().TILE_WIDTH * 4
        )


class Inky(Ghost):
    def __init__(self, node, pac_man=None, blinky=None):
        Ghost.__init__(self, node, pac_man, blinky)
        self.name = Character().INKY
        self.color = "aqua"
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Vector2(
            Display().TILE_WIDTH * Display().N_COLS,
            Display().TILE_HEIGHT * Display().N_ROWS,
        )

    def chase(self):
        vector1 = (
            self.pac_man.position
            + self.pac_man.directions[self.pac_man.direction] * Display().TILE_WIDTH * 2
        )
        vector2 = (vector1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vector2


class Clyde(Ghost):
    def __init__(self, node, pac_man=None, blinky=None):
        Ghost.__init__(self, node, pac_man, blinky)
        self.name = Character().CLYDE
        self.color = "#FFB852"
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Vector2(0, Display().TILE_HEIGHT * Display().N_ROWS)

    def chase(self):
        distance = self.pac_man.position - self.position
        distance_squared = distance.magnitude_squared()
        if distance_squared <= (Display().TILE_WIDTH * 8) ** 2:
            self.scatter()
        else:
            self.goal = (
                self.pac_man.position
                + self.pac_man.directions[self.pac_man.direction]
                * Display().TILE_WIDTH
                * 4
            )


class GhostGroup(object):
    def __init__(self, node, pac_man):
        self.blinky = Blinky(node, pac_man)
        self.pinky = Pinky(node, pac_man)
        self.inky = Inky(node, pac_man, self.blinky)
        self.clyde = Clyde(node, pac_man)
        self.ghost_list = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        return iter(self.ghost_list)

    def set_spawn_node(self, node):
        for ghost in self:
            ghost.set_spawn_node(node)

    def render(self, screen):
        for ghost in self:
            ghost.render(screen)

    def show(self):
        for ghost in self:
            ghost.visibility = True

    def hide(self):
        for ghost in self:
            ghost.visibility = False

    def initial_fright_state(self):
        for ghost in self:
            ghost.initial_fright_state()
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
