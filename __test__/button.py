import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, K_RETURN, QUIT


class Button(pygame.sprite.Sprite):
    def __init__(self):
        super(Button, self).__init__()
        pygame.init()
        pygame.display.set_caption("Button Demo")
        self.screen = pygame.display.set_mode(size=(448, 512))
        self.font = pygame.font.Font("assets/font/8bit_wonder.ttf", 36)
        self.render_font = self.font.render("Start", True, "white")
        self.surface = self.render_font.get_rect(center=(448 / 2, 512 / 2))
        self.click = None
        self.button = None
        self.running = None
        self.frame_rate = None
        self.render_counter = None
        self.counter = 0

    def render(self):
        self.screen.blit(self.render_font, self.surface)

    def clicked(self):
        player_action = False
        mouse_position = pygame.mouse.get_pos()
        if self.surface.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1 and self.click is False:
                player_action = True
                self.click = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.click = False
        return player_action

    def update(self):
        self.button = Button()

        while self.running:
            self.frame_rate = pygame.time.Clock().tick(360) / 1000
            self.screen.fill("black")
            for event in pygame.event.get():
                if self.button.clicked():
                    print("Clicked")
                    self.counter += 1
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        print("Returned")
                        self.counter += 1
                    elif event.key == K_ESCAPE:
                        self.running = False
                elif event.type == QUIT:
                    self.running = False
            if self.running:
                self.button.render()
            self.render_counter = pygame.font.Font(
                "assets/font/8bit_wonder.ttf", 36
            ).render(str(self.counter), True, "Red")
            self.screen.blit(self.render_counter, (448 / 3.3, 512 / 1.7))
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    executing = Button()
    while executing.running:
        executing.update()
