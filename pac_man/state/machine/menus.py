import pygame

from pac_man.assets.sprites.characters.pac_man import PacMan
from pac_man.run import GameController
from references import References
from pac_man.utils.enums.display.display import Display
from pac_man.utils.enums.display.state.machine.select import Select


class StateMachine(PacMan, References, GameController):
    def __init__(self, node, run_display=True):
        PacMan.__init__(self, node)
        References.__init__(self)
        GameController.__init__(self)
        self.run_display = run_display
        self.cursor = pygame.Rect(0, 0, 20, 20)

    def cursor_drawing(self):
        self.state_menu_text("!", 15, self.cursor.x, self.cursor.y)

    def surface_drawing(self):
        self.screen.blit(self.display_surface, (0, 0))
        pygame.display.flip()
        self.reset_keys()


class MainMenu(StateMachine):
    def __init__(self, node, run_display=True):
        StateMachine.__init__(self, node)
        self.run_display = run_display
        self.THE_STATE = Select().START_GAME
        self.cursor.midtop = (
            Display().SCREEN_MID_WIDTH - 100,
            Display().SCREEN_MID_HEIGHT - 40,
        )

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.player_input()
            self.display_surface.fill("Black")
            self.start_menu(335, 84, (49, 455 // 3.77), 351, 100, (57, 449 // 3.49))
            self.state_menu_text(
                Select().START_GAME,
                36,
                Display().SCREEN_MID_WIDTH,
                Display().SCREEN_MID_HEIGHT - 40,
            )
            self.state_menu_text(
                Select().OPTIONS,
                36,
                Display().SCREEN_MID_WIDTH,
                Display().SCREEN_MID_HEIGHT,
            )
            self.state_menu_text(
                Select().CREDITS,
                36,
                Display().SCREEN_MID_WIDTH,
                Display().SCREEN_MID_HEIGHT + 40,
            )
            self.cursor_drawing()
            self.state_menu_custom_text(
                "pacco",
                27,
                Display().SCREEN_MID_WIDTH,
                Display().SCREEN_MID_HEIGHT + 140,
            )
            self.images()
            self.surface_drawing()

    def cursor_position(self):
        if self.DOWN_K:
            if self.THE_STATE == Select().START_GAME:
                self.cursor.midtop = (
                    Display().SCREEN_MID_WIDTH - 80,
                    Display().SCREEN_MID_HEIGHT,
                )
                self.THE_STATE = Select().OPTIONS
            elif self.THE_STATE == Select().OPTIONS:
                self.cursor.midtop = (
                    Display().SCREEN_MID_WIDTH - 80,
                    Display().SCREEN_MID_HEIGHT + 40,
                )
                self.THE_STATE = Select().CREDITS
            elif self.THE_STATE == Select().CREDITS:
                self.cursor.midtop = (
                    Display().SCREEN_MID_WIDTH - 101,
                    Display().SCREEN_MID_HEIGHT - 40,
                )
                self.THE_STATE = Select().START_GAME
        elif self.UP_K:
            if self.THE_STATE == Select().START_GAME:
                self.cursor.midtop = (
                    Display().SCREEN_MID_WIDTH - 80,
                    Display().SCREEN_MID_HEIGHT + 40,
                )
                self.THE_STATE = Select().CREDITS
            elif self.THE_STATE == Select().CREDITS:
                self.cursor.midtop = (
                    Display().SCREEN_MID_WIDTH - 80,
                    Display().SCREEN_MID_HEIGHT,
                )
                self.THE_STATE = Select().OPTIONS
            elif self.THE_STATE == Select().OPTIONS:
                self.cursor.midtop = (
                    Display().SCREEN_MID_WIDTH - 101,
                    Display().SCREEN_MID_HEIGHT - 40,
                )
                self.THE_STATE = Select().START_GAME

    def player_input(self):
        self.cursor_position()
        if self.START_K:
            if self.THE_STATE == Select().START_GAME:
                self.playing = True
            elif self.THE_STATE == Select().OPTIONS:
                self.current = self.options
                self.playing = False
            elif self.THE_STATE == Select().CREDITS:
                self.current = self.acknowledgements
                self.playing = False
            self.run_display = False


class OptionsMenu(StateMachine):
    def __init__(self, node, run_display=True):
        StateMachine.__init__(self, node)
        self.run_display = run_display
        self.THE_STATE = Select().VOLUME
        self.cursor.midtop = (
            Display().SCREEN_MID_WIDTH - 70,
            Display().SCREEN_MID_HEIGHT - 40,
        )

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.player_input()
            self.display_surface.fill("Black")
            self.options_menu(335, 84, (49, 455 // 3.77), 351, 100, (57, 449 // 3.49))
            self.state_menu_text(
                Select().VOLUME,
                36,
                Display().SCREEN_MID_WIDTH,
                Display().SCREEN_MID_HEIGHT - 40,
            )
            self.state_menu_text(
                Select().CONTROLS,
                36,
                Display().SCREEN_MID_WIDTH,
                Display().SCREEN_MID_HEIGHT,
            )
            self.state_menu_text(
                Select().GRAPHICS,
                36,
                Display().SCREEN_MID_WIDTH,
                Display().SCREEN_MID_HEIGHT + 40,
            )
            self.cursor_drawing()
            self.state_menu_custom_text(
                "pacco",
                27,
                Display().SCREEN_MID_WIDTH,
                Display().SCREEN_MID_HEIGHT + 140,
            )
            self.images()
            self.surface_drawing()

    def cursor_position(self):
        if self.DOWN_K:
            if self.THE_STATE == Select().VOLUME:
                self.cursor.midtop = (
                    Display().SCREEN_MID_WIDTH - 90,
                    Display().SCREEN_MID_HEIGHT,
                )
                self.THE_STATE = Select().CONTROLS
            elif self.THE_STATE == Select().CONTROLS:
                self.cursor.midtop = (
                    Display().SCREEN_MID_WIDTH - 90,
                    Display().SCREEN_MID_HEIGHT + 40,
                )
                self.THE_STATE = Select().GRAPHICS
            elif self.THE_STATE == Select().GRAPHICS:
                self.cursor.midtop = (
                    Display().SCREEN_MID_WIDTH - 70,
                    Display().SCREEN_MID_HEIGHT - 40,
                )
                self.THE_STATE = Select().VOLUME
        elif self.UP_K:
            if self.THE_STATE == Select().VOLUME:
                self.cursor.midtop = (
                    Display().SCREEN_MID_WIDTH - 90,
                    Display().SCREEN_MID_HEIGHT + 40,
                )
                self.THE_STATE = Select().GRAPHICS
            elif self.THE_STATE == Select().GRAPHICS:
                self.cursor.midtop = (
                    Display().SCREEN_MID_WIDTH - 90,
                    Display().SCREEN_MID_HEIGHT,
                )
                self.THE_STATE = Select().CONTROLS
            elif self.THE_STATE == Select().CONTROLS:
                self.cursor.midtop = (
                    Display().SCREEN_MID_WIDTH - 70,
                    Display().SCREEN_MID_HEIGHT - 40,
                )
                self.THE_STATE = Select().VOLUME

    def player_input(self):
        self.cursor_position()
        if self.BACK_K:
            self.__init__.current = self.main
            self.run_display = False


class CreditsMenu(StateMachine):
    def __init__(self, node, run_display=True):
        StateMachine.__init__(self, node)
        self.run_display = run_display

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            if self.BACK_K:
                self.__init__.current = self.main
                self.run_display = False
            self.display_surface.fill("Black")
            self.credits_menu(335, 84, (49, 455 // 3.77), 351, 100, (57, 449 // 3.49))
            self.state_menu_text(
                "Made by",
                36,
                Display().SCREEN_MID_WIDTH,
                Display().SCREEN_MID_HEIGHT - 40,
            )
            self.credits(
                "Michael D Johnson",
                27,
                Display().SCREEN_MID_WIDTH,
                Display().SCREEN_MID_HEIGHT + 5,
            )
            self.state_menu_text(
                "And inspired by",
                36,
                Display().SCREEN_MID_WIDTH,
                Display().SCREEN_MID_HEIGHT + 50,
            )
            self.credits(
                "CDcodes",
                36,
                Display().SCREEN_MID_WIDTH,
                Display().SCREEN_MID_HEIGHT + 100,
            )
            self.surface_drawing()
