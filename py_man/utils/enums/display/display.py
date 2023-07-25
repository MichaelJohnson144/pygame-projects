class Display:
    def __init__(self):
        self.TILE_WIDTH, self.TILE_HEIGHT = 16, 16
        self.N_ROWS, self.N_COLS = 36, 28
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = (
            self.N_COLS * self.TILE_WIDTH,
            self.N_ROWS * self.TILE_HEIGHT,
        )
        self.SCREEN_SIZE = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        self.SCREEN_MID_WIDTH, self.SCREEN_MID_HEIGHT = (
            self.SCREEN_WIDTH // 2,
            self.SCREEN_HEIGHT // 2,
        )
