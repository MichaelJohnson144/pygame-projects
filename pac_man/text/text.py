import pygame

from pac_man.utils.enums.display.display import Display
from pac_man.utils.enums.display.font.font_family import FontFamily
from pac_man.utils.enums.display.state.executing.executing import Executing
from pac_man.vector.vector import Vector2


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
            x, y = self.position.tuple()
            screen.blit(self.label, (x, y))

    def update(self, dt):
        if self.lifespan is not None:
            self.timer += dt
            if self.timer >= self.lifespan:
                self.timer = 0
                self.lifespan = None
                self.destroy = True


class TextGroup(object):
    def __init__(self, size=None):
        self.next_identification = 10
        self.text_dictionary = {}
        self.size = size
        self.setup_text()
        self.show_text(Executing().READY_TEXT)

    def setup_text(self):
        self.size = Display().TILE_HEIGHT
        self.text_dictionary[Executing().SCORE_TEXT] = Text(
            "0".zfill(8), "white", 0, Display().TILE_HEIGHT, self.size
        )
        self.text_dictionary[Executing().HIGH_SCORE_TEXT] = Text(
            "0".zfill(8),
            "white",
            11 * Display().TILE_WIDTH,
            Display().TILE_HEIGHT,
            self.size,
        )
        self.text_dictionary[Executing().LEVEL_TEXT] = Text(
            str(1).zfill(3),
            "white",
            23 * Display().TILE_WIDTH,
            Display().TILE_HEIGHT,
            self.size,
        )
        self.text_dictionary[Executing().READY_TEXT] = Text(
            "READY!",
            "yellow",
            11.25 * Display().TILE_WIDTH,
            20 * Display().TILE_HEIGHT,
            self.size,
            visible=False,
        )
        self.text_dictionary[Executing().PAUSE_TEXT] = Text(
            "PAUSED!",
            "yellow",
            10.625 * Display().TILE_WIDTH,
            20 * Display().TILE_HEIGHT,
            self.size,
            visible=False,
        )
        self.text_dictionary[Executing().GAME_OVER_TEXT] = Text(
            "GAMEOVER!",
            "yellow",
            10 * Display().TILE_WIDTH,
            20 * Display().TILE_HEIGHT,
            self.size,
            visible=False,
        )
        self.add_text("SCORE", "white", 0, 0, self.size)
        self.add_text("HIGH SCORE", "white", 10 * Display().TILE_WIDTH, 0, self.size)
        self.add_text("LEVEL", "white", 23 * Display().TILE_WIDTH, 0, self.size)

    def add_text(self, text, color, x, y, size, time=None, identification=None):
        self.next_identification += 1
        self.text_dictionary[self.next_identification] = Text(
            text, color, x, y, size, time=time, identification=identification
        )
        return self.next_identification

    def render(self, screen):
        for text_key in list(self.text_dictionary.keys()):
            self.text_dictionary[text_key].render(screen)

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
        self.text_dictionary[Executing().READY_TEXT].visible = False
        self.text_dictionary[Executing().PAUSE_TEXT].visible = False
        self.text_dictionary[Executing().GAME_OVER_TEXT].visible = False

    def update(self, dt):
        for text_key in list(self.text_dictionary.keys()):
            self.text_dictionary[text_key].update(dt)
            if self.text_dictionary[text_key].destroy:
                self.remove_text(text_key)
