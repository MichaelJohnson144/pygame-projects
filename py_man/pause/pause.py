class Pause(object):
    def __init__(self, paused=False):
        self.pause_time = None
        self.timer = 0
        self.paused = paused
        self.is_paused = None
        self.function = None

    def update(self, dt):
        if self.pause_time is not None:
            self.timer += dt
            if self.timer >= self.pause_time:
                self.timer = 0
                self.paused = False
                self.pause_time = None
                return self.function

    def set_pause(self, pause=False, pause_time=None, function=None):
        self.is_paused = pause
        self.pause_time = pause_time
        self.timer = 0
        self.function = function
        self.flip_display()

    def flip_display(self):
        self.paused = not self.paused
