from py_man.utils.enums.direction.state.ghost_state.ghost_state import GhostState


class OriginalState(object):
    def __init__(self):
        self.state = None
        self.ghost_state = GhostState()
        self.time = None
        self.timer = 0
        self.scatter()

    def scatter(self):
        self.state = self.ghost_state.SCATTER
        self.time = 7
        self.timer = 0

    def chase(self):
        self.state = self.ghost_state.CHASE
        self.time = 20
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.time:
            (self.chase if self.state is self.ghost_state.SCATTER else self.scatter)()


class StateController(object):
    def __init__(self, entity):
        self.original_state = OriginalState()
        self.current = self.original_state.state
        self.ghost_state = GhostState()
        self.timer = 0
        self.time = None
        self.frightened_time = 6
        self.blinking_time = 1
        self.entity = entity

    def spawn(self):
        if self.current is self.ghost_state.FRIGHTENED:
            self.current = self.ghost_state.SPAWN

    def frightened(self):
        if self.current in [
            self.ghost_state.SCATTER,
            self.ghost_state.CHASE,
            self.ghost_state.FRIGHTENED,
            self.ghost_state.BLINKING,
        ]:
            self.timer = 0
            self.time = self.frightened_time
            self.current = self.ghost_state.FRIGHTENED

    def blinking(self):
        if (
            self.current == self.ghost_state.FRIGHTENED
            and self.timer >= self.frightened_time
        ):
            self.timer = 0
            self.time = self.blinking_time
            self.current = self.ghost_state.BLINKING

    def reset(self):
        self.time = None
        self.entity.original_state()
        self.current = self.original_state.state

    def handle_scatter_state(self):
        self.reset()

    def handle_chase_state(self):
        self.reset()

    def handle_frightened_state(self):
        if self.timer >= self.frightened_time:
            self.blinking()

    def handle_blinking_state(self):
        if self.timer >= self.blinking_time - 1:
            self.reset()

    def handle_spawn_state(self):
        if self.entity.node == self.entity.spawn_point_node:
            self.reset()

    def update(self, dt):
        self.timer += dt
        state_to_function = {
            self.ghost_state.SCATTER: self.handle_scatter_state,
            self.ghost_state.CHASE: self.handle_chase_state,
            self.ghost_state.FRIGHTENED: self.handle_frightened_state,
            self.ghost_state.BLINKING: self.handle_blinking_state,
            self.ghost_state.SPAWN: self.handle_spawn_state,
        }
        if self.current in state_to_function:
            state_to_function[self.current]()
        self.original_state.update(dt)
