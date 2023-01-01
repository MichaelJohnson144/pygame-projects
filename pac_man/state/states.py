from pac_man.utils.enums.direction.state.ghost_state.ghost_state import GhostState


class OriginalState(object):
    def __init__(self):
        self.timer = 0
        self.time = None
        self.mode = None
        self.scatter()

    def scatter(self):
        self.mode = GhostState().SCATTER
        self.time = 7
        self.timer = 0

    def chase(self):
        self.mode = GhostState().CHASE
        self.time = 20
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is GhostState().SCATTER:
                self.chase()
            elif self.mode is GhostState().CHASE:
                self.scatter()


class StateController(object):
    def __init__(self, entity):
        self.timer = 0
        self.time = None
        self.original_state = OriginalState()
        self.current = self.original_state.mode
        self.entity = entity

    def set_spawn_state(self):
        if self.current is GhostState().FRIGHTENED:
            self.current = GhostState().SPAWN

    def set_freight_state(self):
        if self.current in [GhostState().SCATTER, GhostState().CHASE]:
            self.timer = 0
            self.time = 7
            self.current = GhostState().FRIGHTENED
        elif self.current is GhostState().FRIGHTENED:
            self.timer = 0

    def update(self, dt):
        self.original_state.update(dt)
        if self.current is GhostState().FRIGHTENED:
            self.timer += dt
            if self.timer >= self.time:
                self.time = None
                self.entity.original_state()
                self.current = self.original_state.mode
        elif self.current in [GhostState().SCATTER, GhostState().CHASE]:
            self.current = self.original_state.mode

        if (
            self.current is GhostState().SPAWN
            and self.entity.node == self.entity.spawn_node
        ):
            self.entity.original_state()
            self.current = self.original_state.mode
