class Animation(object):
    def __init__(self, frame_array=None, speed=20, loop=True):
        self.current_frame = 0
        self.finished = False
        self.dt = 0
        self.speed = speed
        if frame_array is None:
            frame_array = []
        self.frame_array = frame_array
        self.loop = loop

    def reset_frame(self):
        self.current_frame = 0
        self.finished = False

    def next_frame(self, dt):
        self.dt += dt
        if self.dt >= (1.0 / self.speed):
            self.current_frame += 1
            self.dt = 0

    def update_frame(self, dt):
        if not self.finished:
            self.next_frame(dt)
        if self.current_frame >= len(self.frame_array):
            if self.loop:
                self.current_frame = 0
            else:
                self.current_frame -= 1
                self.finished = True
        return self.frame_array[self.current_frame]
