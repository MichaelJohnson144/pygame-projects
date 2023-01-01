import numpy as np
import pygame

from pac_man.animation.animation import Animation
from pac_man.utils.enums.direction.joypad.joypad import Joypad
from pac_man.utils.enums.direction.state.ghost_state.ghost_state import GhostState
from pac_man.utils.enums.display.character.character import Character
from pac_man.utils.enums.display.display import Display


class SpriteSheet(object):
    def __init__(self):
        self.sprite_sheet = pygame.image.load(
            "assets/sprites/sprite_sheets/pac-man.png"
        ).convert()
        transparent_color = self.sprite_sheet.get_at((0, 0))
        self.sprite_sheet.set_colorkey(transparent_color)
        width = int(self.sprite_sheet.get_width() / 16 * Display().TILE_WIDTH)
        height = int(self.sprite_sheet.get_height() / 16 * Display().TILE_HEIGHT)
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (width, height))

    # "Extract" a "sprite" from the "sprite sheet" upon request:
    def get_sprite(self, x, y, width, height):
        x *= Display().TILE_WIDTH
        y *= Display().TILE_HEIGHT
        self.sprite_sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sprite_sheet.subsurface(self.sprite_sheet.get_clip())


# This class will contain references to all the "'Pac-Man' sprites:"
class PacManSprites(SpriteSheet):
    def __init__(self, pac_man):
        SpriteSheet.__init__(self)
        self.animation_dictionary = {}
        self.define_animations()
        self.pac_man = pac_man
        self.pac_man.sprite = self.return_initial_sprite()
        self.stop_sprite = (8, 0)

    def define_animations(self):
        self.animation_dictionary[Joypad().UP] = Animation(
            ((10, 2), (6, 0), (6, 2), (6, 0))
        )
        self.animation_dictionary[Joypad().RIGHT] = Animation(
            ((10, 0), (2, 0), (2, 2), (2, 0))
        )
        self.animation_dictionary[Joypad().DOWN] = Animation(
            ((8, 2), (4, 0), (4, 2), (4, 0))
        )
        self.animation_dictionary[Joypad().LEFT] = Animation(
            ((8, 0), (0, 0), (0, 2), (0, 0))
        )
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

    # "Extract" Pac-Man's "sprite" from the "sprite sheet" upon "request:"
    def get_sprite(self, x, y, width, height):
        return SpriteSheet.get_sprite(
            self, x, y, 2 * Display().TILE_WIDTH, 2 * Display().TILE_HEIGHT
        )

    # "Return" Pac-Man's "beginning sprite" upon "'initial' execution:"
    def return_initial_sprite(self):
        return self.get_sprite(8, 0, width=self, height=self)

    def update(self, dt):
        if self.pac_man.alive:
            if self.pac_man.direction == Joypad().LEFT:
                self.pac_man.sprite = self.get_sprite(
                    *self.animation_dictionary[Joypad().LEFT].update_frame(dt),
                    width=self,
                    height=self
                )
                self.stop_sprite = (8, 0)
            elif self.pac_man.direction == Joypad().RIGHT:
                self.pac_man.sprite = self.get_sprite(
                    *self.animation_dictionary[Joypad().RIGHT].update_frame(dt),
                    width=self,
                    height=self
                )
                self.stop_sprite = (10, 0)
            elif self.pac_man.direction == Joypad().DOWN:
                self.pac_man.sprite = self.get_sprite(
                    *self.animation_dictionary[Joypad().DOWN].update_frame(dt),
                    width=self,
                    height=self
                )
                self.stop_sprite = (8, 2)
            elif self.pac_man.direction == Joypad().UP:
                self.pac_man.sprite = self.get_sprite(
                    *self.animation_dictionary[Joypad().UP].update_frame(dt),
                    width=self,
                    height=self
                )
                self.stop_sprite = (10, 2)
            elif self.pac_man.direction == Joypad().STOP:
                self.pac_man.sprite = self.get_sprite(
                    *self.stop_sprite, width=self, height=self
                )
        else:
            self.pac_man.sprite = self.get_sprite(
                *self.animation_dictionary[5].update_frame(dt), width=self, height=self
            )

    def reset(self):
        for key in list(self.animation_dictionary.keys()):
            self.animation_dictionary[key].reset_frame()


# This class will contain references to all the "'Ghost' sprites:"
class GhostSprites(SpriteSheet):
    def __init__(self, ghost):
        SpriteSheet.__init__(self)
        self.x = {
            Character().BLINKY: 0,
            Character().PINKY: 2,
            Character().INKY: 4,
            Character().CLYDE: 6,
        }
        self.ghost = ghost
        self.ghost.sprite = self.return_initial_sprite()

    # "Extract" the Ghosts' "sprites" from the "sprite sheet" upon "request:"
    def get_sprite(self, x, y, width, height):
        return SpriteSheet.get_sprite(
            self, x, y, 2 * Display().TILE_WIDTH, 2 * Display().TILE_HEIGHT
        )

    # "Return" the Ghosts' "beginning sprites" upon "'initial' execution:"
    def return_initial_sprite(self):
        return self.get_sprite(self.x[self.ghost.name], 4, width=self, height=self)

    def update(self, dt):
        x = self.x[self.ghost.name]
        if self.ghost.mode.current in [GhostState().SCATTER, GhostState().CHASE]:
            if self.ghost.direction == Joypad().LEFT:
                self.ghost.sprite = self.get_sprite(x, 8, width=self, height=self)
            elif self.ghost.direction == Joypad().RIGHT:
                self.ghost.sprite = self.get_sprite(x, 10, width=self, height=self)
            elif self.ghost.direction == Joypad().DOWN:
                self.ghost.sprite = self.get_sprite(x, 6, width=self, height=self)
            elif self.ghost.direction == Joypad().UP:
                self.ghost.sprite = self.get_sprite(x, 4, width=self, height=self)
        elif self.ghost.mode.current == GhostState().FRIGHTENED:
            self.ghost.sprite = self.get_sprite(10, 4, width=self, height=self)
        elif self.ghost.mode.current == GhostState().SPAWN:
            if self.ghost.direction == Joypad().LEFT:
                self.ghost.sprite = self.get_sprite(8, 8, width=self, height=self)
            elif self.ghost.direction == Joypad().RIGHT:
                self.ghost.sprite = self.get_sprite(8, 10, width=self, height=self)
            elif self.ghost.direction == Joypad().DOWN:
                self.ghost.sprite = self.get_sprite(8, 6, width=self, height=self)
            elif self.ghost.direction == Joypad().UP:
                self.ghost.sprite = self.get_sprite(8, 4, width=self, height=self)


# This class will contain references to all the "'Fruit' sprites:"
class FruitSprites(SpriteSheet):
    def __init__(self, fruit, level):
        SpriteSheet.__init__(self)
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

    # "Extract" the Fruits' "sprites" from the "sprite sheet" upon "request:"
    def get_sprite(self, x, y, width, height):
        return SpriteSheet.get_sprite(
            self, x, y, 2 * Display().TILE_WIDTH, 2 * Display().TILE_HEIGHT
        )

    # "Return" the Fruits' "beginning sprites" upon "'initial' execution:"
    def return_initial_sprite(self, key):
        return self.get_sprite(*self.fruit_dictionary[key], width=self, height=self)


# This class will contain references to all the "'Life' sprites:"
class LifeSprites(SpriteSheet):
    def __init__(self, life_quantity, life_array=None):
        SpriteSheet.__init__(self)
        self.life_array = life_array
        self.reset_lives(life_quantity)

    def get_sprite(self, x, y, width, height):
        return SpriteSheet.get_sprite(
            self, x, y, 2 * Display().TILE_WIDTH, 2 * Display().TILE_HEIGHT
        )

    def remove_sprite(self):
        if len(self.life_array) > 0:
            self.life_array.pop(0)

    def reset_lives(self, life_quantity):
        self.life_array = []
        for i in range(life_quantity):
            self.life_array.append(self.get_sprite(0, 0, width=self, height=self))


# This class will contain references to all the "'Maze' sprites:"
class MazeSprites(SpriteSheet):
    def __init__(self, maze_file, rotated_maze_file):
        SpriteSheet.__init__(self)
        self.maze_file_data = self.read_maze_file(maze_file)
        # "Rotate" the maze file's "'wall' data" so that "'maze wall' sprites" may "'align' and 'unite' correctly:"
        self.rotated_maze_file_data = self.read_maze_file(rotated_maze_file)

    def read_maze_file(self, maze_file):
        return self and np.loadtxt(maze_file, dtype="<U1")

    def construct_maze(self, maze, y):
        for i in list(range(self.maze_file_data.shape[0])):
            for j in list(range(self.maze_file_data.shape[1])):
                if self.maze_file_data[i][j].isdigit():
                    x = int(self.maze_file_data[i][j]) + 12
                    maze_sprite = self.get_sprite(x, y, width=self, height=self)
                    rotated_maze_file_data = int(self.rotated_maze_file_data[i][j])
                    maze_sprite = self.rotate_sprite(maze_sprite, rotated_maze_file_data)
                    maze.blit(
                        maze_sprite, (j * Display().TILE_WIDTH, i * Display().TILE_HEIGHT)
                    )
                elif self.maze_file_data[i][j] == "=":
                    maze_sprite = self.get_sprite(10, 8, width=self, height=self)
                    maze.blit(
                        maze_sprite, (j * Display().TILE_WIDTH, i * Display().TILE_HEIGHT)
                    )
        return maze

    def get_sprite(self, x, y, width, height):
        return SpriteSheet.get_sprite(
            self, x, y, Display().TILE_WIDTH, Display().TILE_HEIGHT
        )

    def rotate_sprite(self, sprite, value):
        return self and pygame.transform.rotate(sprite, value * 90)
