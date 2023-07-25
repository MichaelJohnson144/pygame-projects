import random

import pygame
from pygame.locals import K_UP, K_RIGHT, K_DOWN, K_LEFT, KEYDOWN, K_RETURN, K_ESCAPE, QUIT

pygame.init()
pygame.display.set_caption("Aerial Evader")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.screen = pygame.display.set_mode(
            (800, 600),
            pygame.DOUBLEBUF | pygame.HWSURFACE,
        )
        self.image = pygame.transform.scale(
            pygame.image.load("assets/images/jet.png"), (int(920 / 11), int(550 / 11))
        )
        self.rect = self.image.get_rect()

    def update(self, pressed_keys):
        self.rect.y -= pressed_keys[K_UP] * 17
        self.rect.x += pressed_keys[K_RIGHT] * 17
        self.rect.y += pressed_keys[K_DOWN] * 17
        self.rect.x -= pressed_keys[K_LEFT] * 17
        self.rect.clamp_ip(self.screen.get_rect())


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("assets/images/missile.png"), (int(310 / 8), int(230 / 8))
        )
        self.rect = self.image.get_rect(
            center=(random.randint(800, 900), random.randint(0, 600))
        )
        self.speed = random.uniform(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super(Explosion, self).__init__()
        self.explosion_image = pygame.image.load(
            "assets/images/explosions/explosion.png"
        ).convert_alpha()
        self.frame_width = self.explosion_image.get_width() // 12
        self.frame_height = self.explosion_image.get_height()
        self.explosion_array = [
            self.explosion_image.subsurface(
                pygame.Rect(
                    (i * self.frame_width, 0), (self.frame_width, self.frame_height)
                )
            )
            for i in range(12)
        ]
        self.index = 0
        self.image = self.explosion_array[self.index]
        self.rect = self.image.get_rect(center=center)
        self.frame_rate = 0

    def update_frame(self):
        frame_delay = 1.25
        self.frame_rate += 1
        if self.frame_rate >= frame_delay:
            self.frame_rate = 0
            self.index += 1

    def update_explosion_animation(self):
        if self.index >= len(self.explosion_array):
            self.kill()
        else:
            self.image = self.explosion_array[self.index]

    def update(self):
        self.update_frame()
        self.update_explosion_animation()


class StartText(pygame.sprite.Sprite):
    def __init__(self):
        super(StartText, self).__init__()
        self.screen = pygame.display.set_mode(
            (800, 600),
            pygame.DOUBLEBUF | pygame.HWSURFACE,
        )
        self.font = pygame.font.Font("assets/fonts/8-BIT WONDER.ttf", 36)
        self.render_font = self.font.render("Start", True, "Black")
        self.surface = self.render_font.get_rect(center=(400, 300))
        self.click_limiter = False

    def render(self):
        self.screen.blit(self.render_font, self.surface)

    def is_clicked(self):
        mouse_position = pygame.mouse.get_pos()
        if self.surface.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1 and not self.click_limiter:
                self.click_limiter = True
                return True
        elif pygame.mouse.get_pressed()[0] == 0:
            self.click_limiter = False
        return False


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (800, 600),
            pygame.DOUBLEBUF | pygame.HWSURFACE,
        )
        self.background_surface = pygame.transform.scale(
            pygame.image.load("assets/images/troposphere_bg.png"), (800, 600)
        )
        self.background_surface_position = 0
        self.add_new_enemies = pygame.USEREVENT + 1
        pygame.time.set_timer(self.add_new_enemies, 250)
        self.player = Player()
        self.enemies = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        self.sprite_group = pygame.sprite.Group(self.player)
        self.start_button = StartText()
        self.running, self.playing = True, False

    def handle_events(self):
        for event in pygame.event.get():
            if self.handle_button_events(event):
                continue
            if event.type == KEYDOWN:
                self.handle_keydown_events(event)
            if event.type == QUIT:
                self.running = False
            if event.type == self.add_new_enemies and self.playing:
                self.add_enemy()

    def handle_button_events(self, event):
        if self.start_button.is_clicked() or (
            event.type == KEYDOWN and event.key == K_RETURN
        ):
            self.playing = True
            return True
        if event.type == K_ESCAPE:
            self.running = False
            return True
        return False

    def handle_keydown_events(self, event):
        if event.key == K_ESCAPE:
            self.running = False
        if event.key == K_RETURN:
            self.playing = True

    def add_enemy(self):
        enemy = Enemy()
        self.enemies.add(enemy)
        self.sprite_group.add(enemy)

    def render_screen(self):
        self.screen.fill(pygame.Color("white"))
        background_rect = self.background_surface.get_rect(
            topleft=(self.background_surface_position, 0)
        )
        self.screen.blit(self.background_surface, background_rect)
        self.screen.blit(self.background_surface, (background_rect.right, 0))
        if not self.playing:
            self.start_button.render()

    def update_background(self):
        self.background_surface_position = (self.background_surface_position - 20) % -800

    def update_sprites(self):
        pressed_keys = pygame.key.get_pressed()
        self.player.update(pressed_keys)
        self.enemies.update()
        self.sprite_group.draw(self.screen)
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            explosion_animation = Explosion(self.player.rect.center)
            self.explosion_group.add(explosion_animation)
            self.explosion_group.update()
            self.playing = False
        self.explosion_group.draw(self.screen)
        self.explosion_group.update()

    def run(self):
        while self.running:
            self.handle_events()
            self.render_screen()
            self.update_background()
            self.update_sprites()
            pygame.display.flip()
            # 30 fps is recommended; however, if you desire a challenge, then leave it set to 60:
            pygame.time.Clock().tick(60)
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
