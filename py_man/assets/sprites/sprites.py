import numpy as np
import pygame

from py_man.utils.enums.display.display import Display
from py_man.utils.enums.direction.joypad.joypad import JoyPad
from py_man.utils.enums.display.character.character import Character
from py_man.animation.animation import Animation
from py_man.utils.enums.direction.state.ghost_state.ghost_state import GhostState


class SpriteSheet(object):
    def __init__(self):
        self.sprite_sheet = pygame.image.load(
            "assets/sprites/sprite_sheets/pac-man.png"
        ).convert()
        transparent_color = self.sprite_sheet.get_at((0, 0))
        self.sprite_sheet.set_colorkey(transparent_color)
        self.display = Display()
        width = int(self.sprite_sheet.get_width() / 16 * self.display.TILE_WIDTH)
        height = int(self.sprite_sheet.get_height() / 16 * self.display.TILE_HEIGHT)
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (width, height))
        self.joypad = JoyPad()
        self.name = Character()

    def get_sprite(self, x, y, width, height):
        x *= self.display.TILE_WIDTH
        y *= self.display.TILE_HEIGHT
        self.sprite_sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sprite_sheet.subsurface(self.sprite_sheet.get_clip())


class PyManSprites(SpriteSheet):
    def __init__(self, py_man):
        super().__init__()
        self.animation_dictionary = {}
        self.define_animations()
        self.py_man = py_man
        self.py_man.sprite = self.return_initial_sprite()
        self.stop_sprite = (8, 0)

    def define_animations(self):
        directions = [
            self.joypad.UP,
            self.joypad.RIGHT,
            self.joypad.DOWN,
            self.joypad.LEFT,
        ]
        animations = [
            ((10, 2), (6, 0), (6, 2), (6, 0)),
            ((10, 0), (2, 0), (2, 2), (2, 0)),
            ((8, 2), (4, 0), (4, 2), (4, 0)),
            ((8, 0), (0, 0), (0, 2), (0, 0)),
        ]
        for direction, animation in zip(directions, animations):
            self.animation_dictionary[direction] = Animation(animation)
        self.animation_dictionary[5] = Animation(
            (
                (0, 12),
                (2, 12),
                (4, 12),
                (6, 12),
                (8, 12),
                (10, 12),
                (12, 12),
                (14, 12),
                (16, 12),
                (18, 12),
                (20, 12),
            ),
            speed=6,
            loop=False,
        )

    def get_sprite(self, x, y, width, height):
        return SpriteSheet.get_sprite(
            self, x, y, 2 * self.display.TILE_WIDTH, 2 * self.display.TILE_HEIGHT
        )

    def return_initial_sprite(self):
        return self.get_sprite(8, 0, width=self, height=self)

    def update(self, dt):
        direction = self.py_man.direction
        if not self.py_man.alive:
            sprite_coordinates = self.animation_dictionary[5].update_frame(dt)
        else:
            animation = self.animation_dictionary.get(direction)
            if animation:
                sprite_coordinates = animation.update_frame(dt)
                if direction in [
                    self.joypad.UP,
                    self.joypad.RIGHT,
                    self.joypad.DOWN,
                    self.joypad.LEFT,
                ]:
                    self.stop_sprite = {
                        self.joypad.UP: (10, 2),
                        self.joypad.RIGHT: (10, 0),
                        self.joypad.DOWN: (8, 2),
                        self.joypad.LEFT: (8, 0),
                    }[direction]
            else:
                sprite_coordinates = self.stop_sprite
        self.py_man.sprite = self.get_sprite(*sprite_coordinates, width=self, height=self)

    def reset(self):
        for key in list(self.animation_dictionary.keys()):
            self.animation_dictionary[key].reset_frame()


class GhostSprites(SpriteSheet):
    def __init__(self, ghost):
        super().__init__()
        self.x = {
            self.name.BLINKY: 0,
            self.name.PINKY: 2,
            self.name.INKY: 4,
            self.name.CLYDE: 6,
        }
        self.ghost = ghost
        self.ghost.sprite = self.return_initial_sprite()
        self.ghost_state = GhostState()

    def get_sprite(self, x, y, width, height):
        return SpriteSheet.get_sprite(
            self, x, y, 2 * self.display.TILE_WIDTH, 2 * self.display.TILE_HEIGHT
        )

    def return_initial_sprite(self):
        return self.get_sprite(self.x[self.ghost.name], 4, width=self, height=self)

    def update(self, dt):
        x = self.x[self.ghost.name]
        mode = self.ghost.state_controller.current
        sprites = {
            self.ghost_state.SCATTER: {
                self.joypad.UP: (x, 4),
                self.joypad.RIGHT: (x, 10),
                self.joypad.DOWN: (x, 6),
                self.joypad.LEFT: (x, 8),
            },
            self.ghost_state.CHASE: {
                self.joypad.UP: (x, 4),
                self.joypad.RIGHT: (x, 10),
                self.joypad.DOWN: (x, 6),
                self.joypad.LEFT: (x, 8),
            },
            self.ghost_state.FRIGHTENED: {
                self.joypad.UP: (10, 4),
                self.joypad.RIGHT: (10, 4),
                self.joypad.DOWN: (10, 4),
                self.joypad.LEFT: (10, 4),
            },
            self.ghost_state.BLINKING: {
                self.joypad.UP: (10, 6),
                self.joypad.RIGHT: (10, 6),
                self.joypad.DOWN: (10, 6),
                self.joypad.LEFT: (10, 6),
            },
            self.ghost_state.SPAWN: {
                self.joypad.UP: (8, 4),
                self.joypad.RIGHT: (8, 10),
                self.joypad.DOWN: (8, 6),
                self.joypad.LEFT: (8, 8),
            },
        }
        direction = self.ghost.direction
        sprite_coordinates = sprites[mode].get(direction, (x, 4))
        if mode == self.ghost_state.FRIGHTENED or mode == self.ghost_state.BLINKING:
            time_left = (
                self.ghost.state_controller.time - self.ghost.state_controller.timer
            )
            if time_left <= self.ghost.state_controller.frightened_time:
                blink_speed = time_left / self.ghost.state_controller.frightened_time
                if (int(self.ghost.state_controller.timer / blink_speed) % 2) == 0:
                    sprite_coordinates = sprites[self.ghost_state.FRIGHTENED].get(
                        direction, (10, 4)
                    )
                else:
                    sprite_coordinates = sprites[self.ghost_state.BLINKING].get(
                        direction, (10, 6)
                    )
        self.ghost.sprite = self.get_sprite(*sprite_coordinates, width=self, height=self)


class FruitSprites(SpriteSheet):
    def __init__(self, fruit, level):
        super().__init__()
        self.fruit = fruit
        self.fruit_dictionary = {
            0: (16, 8),
            1: (18, 8),
            2: (20, 8),
            3: (16, 10),
            4: (18, 10),
            5: (20, 10),
        }
        self.fruit.sprite = self.return_initial_sprite(level % len(self.fruit_dictionary))

    def get_sprite(self, x, y, width, height):
        return SpriteSheet.get_sprite(
            self, x, y, 2 * self.display.TILE_WIDTH, 2 * self.display.TILE_HEIGHT
        )

    def return_initial_sprite(self, key):
        return self.get_sprite(*self.fruit_dictionary[key], width=self, height=self)


class LifeSprites(SpriteSheet):
    def __init__(self, life_quantity, life_array=None):
        super().__init__()
        self.life_array = life_array
        self.reset_lives(life_quantity)

    def get_sprite(self, x, y, width, height):
        return SpriteSheet.get_sprite(
            self, x, y, 2 * self.display.TILE_WIDTH, 2 * self.display.TILE_HEIGHT
        )

    def remove_sprite(self):
        if len(self.life_array) > 0:
            self.life_array.pop(0)

    def reset_lives(self, life_quantity):
        self.life_array = [
            self.get_sprite(0, 0, width=self, height=self) for _ in range(life_quantity)
        ]


class MazeSprites(SpriteSheet):
    def __init__(self, maze_file, rotated_maze_file):
        super().__init__()
        self.maze_file_data = self.read_maze_file(maze_file)
        self.rotated_maze_file_data = self.read_maze_file(rotated_maze_file)

    def read_maze_file(self, maze_file):
        return self and np.loadtxt(maze_file, dtype="<U1")

    def construct_maze(self, maze, y):
        for i, row in enumerate(self.maze_file_data):
            for j, cell in enumerate(row):
                x = int(cell) + 12 if cell.isdigit() else None
                if x is not None:
                    maze_sprite = self.get_sprite(x, y, width=self, height=self)
                    rotated_cell = int(self.rotated_maze_file_data[i][j])
                    maze_sprite = self.rotate_sprite(maze_sprite, rotated_cell)
                    maze.blit(
                        maze_sprite,
                        (j * self.display.TILE_WIDTH, i * self.display.TILE_HEIGHT),
                    )
                elif cell == "=":
                    maze_sprite = self.get_sprite(10, 8, width=self, height=self)
                    maze.blit(
                        maze_sprite,
                        (j * self.display.TILE_WIDTH, i * self.display.TILE_HEIGHT),
                    )
        return maze

    def get_sprite(self, x, y, width, height):
        return SpriteSheet.get_sprite(
            self, x, y, self.display.TILE_WIDTH, self.display.TILE_HEIGHT
        )

    def rotate_sprite(self, sprite, value):
        return self and pygame.transform.rotate(sprite, value * 90)
