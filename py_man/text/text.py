import pygame
from pygame import Vector2

from py_man.utils.enums.display.font.font_family import FontFamily
from py_man.utils.enums.display.display import Display
from py_man.utils.enums.display.state.executing.executing import Executing


class Text(object):
    def __init__(
        self,
        text,
        color,
        x,
        y,
        size,
        time=None,
        identification=None,
        visible=True,
    ):
        self.font = None
        self.size = size
        self.label = None
        self.font_text = text
        self.color = color
        self.lifespan = time
        self.timer = 0
        self.destroy = False
        self.visible = visible
        self.position = Vector2(x, y)
        self.identification = identification
        self.set_font(FontFamily().PRESS_START_2P)
        self.create_label()

    def set_font(self, font_path):
        self.font = pygame.font.Font(font_path, self.size)

    def create_label(self):
        self.label = self.font.render(self.font_text, 1, self.color)

    def set_text(self, text):
        self.font_text = str(text)
        self.create_label()

    def render(self, screen):
        if self.visible:
            x, y = self.position.x, self.position.y
            screen.blit(self.label, (x, y))

    def update(self, dt):
        self.destroy = self.lifespan is not None and self.timer + dt >= self.lifespan
        self.timer = self.timer % self.lifespan if self.destroy else self.timer + dt
        self.lifespan = None if self.destroy else self.lifespan


class TextGroup(object):
    def __init__(self, size=None):
        self.next_identification = 10
        self.text_dictionary = {}
        self.size = size
        self.display = Display()
        self.executing = Executing()
        self.setup_text()
        self.show_text(self.executing.READY_TEXT)

    def setup_text(self):
        self.size = self.display.TILE_HEIGHT
        self.text_dictionary = {
            Executing().SCORE_TEXT: Text(
                "0".zfill(8), "white", 0, self.display.TILE_HEIGHT, self.size
            ),
            Executing().HIGH_SCORE_TEXT: Text(
                "0".zfill(8),
                "white",
                11 * self.display.TILE_WIDTH,
                self.display.TILE_HEIGHT,
                self.size,
            ),
            Executing().LEVEL_TEXT: Text(
                str(1).zfill(3),
                "white",
                23 * self.display.TILE_WIDTH,
                self.display.TILE_HEIGHT,
                self.size,
            ),
            self.executing.READY_TEXT: Text(
                "READY!",
                "yellow",
                11.25 * self.display.TILE_WIDTH,
                20 * self.display.TILE_HEIGHT,
                self.size,
                visible=False,
            ),
            self.executing.PAUSE_TEXT: Text(
                "PAUSED!",
                "yellow",
                10.625 * self.display.TILE_WIDTH,
                20 * self.display.TILE_HEIGHT,
                self.size,
                visible=False,
            ),
            self.executing.GAME_OVER_TEXT: Text(
                "GAMEOVER!",
                "yellow",
                10 * self.display.TILE_WIDTH,
                20 * self.display.TILE_HEIGHT,
                self.size,
                visible=False,
            ),
            "SCORE": Text("SCORE", "white", 0, 0, self.size),
            "HIGH SCORE": Text(
                "HIGH SCORE", "white", 10 * self.display.TILE_WIDTH, 0, self.size
            ),
            "LEVEL": Text("LEVEL", "white", 23 * self.display.TILE_WIDTH, 0, self.size),
        }

    def add_text(self, text, color, x, y, size, time=None, identification=None):
        new_text = Text(text, color, x, y, size, time=time, identification=identification)
        self.text_dictionary[id(new_text)] = new_text
        return id(new_text)

    def render(self, screen):
        for text in self.text_dictionary.values():
            text.render(screen)

    def show_text(self, identification):
        self.hide_text()
        self.text_dictionary[identification].visible = True

    def update_text(self, identification, value):
        if identification in self.text_dictionary.keys():
            self.text_dictionary[identification].set_text(value)

    def update_score(self, score):
        self.update_text(Executing().SCORE_TEXT, str(score).zfill(8))

    def update_high_score(self, high_score):
        self.update_text(Executing().HIGH_SCORE_TEXT, str(high_score).zfill(8))

    def update_level(self, level):
        self.update_text(Executing().LEVEL_TEXT, str(level + 1).zfill(3))

    def remove_text(self, identification):
        self.text_dictionary.pop(identification)

    def hide_text(self):
        self.text_dictionary[self.executing.READY_TEXT].visible = False
        self.text_dictionary[self.executing.PAUSE_TEXT].visible = False
        self.text_dictionary[self.executing.GAME_OVER_TEXT].visible = False

    def update(self, dt):
        self.text_dictionary = {
            key: value for key, value in self.text_dictionary.items() if not value.destroy
        }
        for text in self.text_dictionary.values():
            text.update(dt)
