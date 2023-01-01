import pygame

from menus import MainMenu, OptionsMenu, CreditsMenu
from pac_man.utils.enums.display.display import Display
from pac_man.utils.enums.display.font.font_family import FontFamily


class References:
    def __init__(self):
        self.playing = True
        self.main = MainMenu(self)
        self.options = OptionsMenu(self)
        self.acknowledgements = CreditsMenu(self)
        self.current = self.main

    def start_menu(self, x_2, y_2, outer_perimeter, x_1, y_1, inner_perimeter):
        outer = pygame.Rect(outer_perimeter, (x_1, y_1))
        inner = pygame.Rect(inner_perimeter, (x_2, y_2))
        crack_man_font = pygame.font.Font(FontFamily().CRACK_MAN, 63)
        render_text = crack_man_font.render("Pac-Man", True, "Black")
        return_text = render_text.get_rect(center=(outer.center and inner.center))
        pygame.draw.rect(Display().SCREEN_WIDTH, "Red", outer, 5, 12)
        pygame.draw.rect(Display().SCREEN_WIDTH, (216, 108, 0), inner, 0, 4)
        Display().SCREEN_WIDTH.blit(render_text, return_text)
        return self

    def options_menu(self, x_2, y_2, outer_perimeter, x_1, y_1, inner_perimeter):
        outer = pygame.Rect(outer_perimeter, (x_1, y_1))
        inner = pygame.Rect(inner_perimeter, (x_2, y_2))
        crack_man_font = pygame.font.Font(FontFamily().CRACK_MAN, 63)
        render_text = crack_man_font.render("Options", True, "Black")
        return_text = render_text.get_rect(center=(outer.center and inner.center))
        pygame.draw.rect(Display().SCREEN_WIDTH, "Red", outer, 5, 12)
        pygame.draw.rect(Display().SCREEN_WIDTH, (216, 108, 0), inner, 0, 4)
        Display().SCREEN_WIDTH.blit(render_text, return_text)
        return self

    def credits_menu(self, x_2, y_2, outer_perimeter, x_1, y_1, inner_perimeter):
        outer = pygame.Rect(outer_perimeter, (x_1, y_1))
        inner = pygame.Rect(inner_perimeter, (x_2, y_2))
        crack_man_font = pygame.font.Font(FontFamily().CRACK_MAN, 63)
        render_text = crack_man_font.render("Credits", True, "Black")
        return_text = render_text.get_rect(center=(outer.center and inner.center))
        pygame.draw.rect(Display().SCREEN_WIDTH, "Red", outer, 5, 12)
        pygame.draw.rect(Display().SCREEN_WIDTH, (216, 108, 0), inner, 0, 4)
        Display().SCREEN_WIDTH.blit(
            render_text,
            return_text,
        )
        return self

    def state_menu_text(self, text, size, x, y):
        arcade_classic_font = pygame.font.Font(FontFamily().ARCADE_CLASSIC, size)
        render_text = arcade_classic_font.render(text, True, "White")
        return_text = render_text.get_rect(center=(x, y))
        Display().SCREEN_WIDTH.blit(render_text, return_text)
        return self

    def state_menu_custom_text(self, text, size, x, y):
        namico_regular_font = pygame.font.Font(FontFamily().NAMICO_REGULAR, size)
        render_text = namico_regular_font.render(text, True, "Red")
        return_text = render_text.get_rect(center=(x, y))
        Display().SCREEN_WIDTH.blit(render_text, return_text)
        return self

    def credits(self, text, size, x, y):
        font = pygame.font.Font(FontFamily().LAB_RAID_8PX, size)
        render_text = font.render(text, True, (216, 108, 0))
        return_text = render_text.get_rect(center=(x, y))
        Display().SCREEN_WIDTH.blit(
            render_text,
            return_text,
        )
        return self

    def images(self):
        image_surface = pygame.image.load("assets/images/The_Ghost_Squad.png")
        image_surface = pygame.transform.scale(
            image_surface, size=(820 // 4.5, 240 // 4.5)
        )
        Display().SCREEN_WIDTH.blit(image_surface, (265 / 2, 695 / 2))
        left_image_surface = pygame.image.load("assets/images/Pac_Man_Left.png")
        left_image_surface = pygame.transform.scale(
            left_image_surface, size=(551 // 7, 391 // 7)
        )
        Display().SCREEN_WIDTH.blit(left_image_surface, (45, 390))
        right_image_surface = pygame.image.load("assets/images/Pac_Man_Right.png")
        right_image_surface = pygame.transform.scale(
            right_image_surface, size=(551 // 7, 391 // 7)
        )
        Display().SCREEN_WIDTH.blit(right_image_surface, (320, 390))
        return self

    def reset_keys(self):
        (
            self.UP_K,
            self.DOWN_K,
            self.RIGHT_K,
            self.LEFT_K,
            self.START_K,
            self.BACK_K,
        ) = (False, False, False, False, False, False)
