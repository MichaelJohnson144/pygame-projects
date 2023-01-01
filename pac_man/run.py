import pygame
from pygame.locals import KEYDOWN, K_RETURN, K_ESCAPE, QUIT

from maze_data.maze_data import MazeData
from nodes.nodes import NodeGroup
from pac_man.assets.sprites.characters.ghosts import GhostGroup
from pac_man.assets.sprites.characters.pac_man import PacMan
from pac_man.assets.sprites.fruit.fruit import Fruit
from pac_man.assets.sprites.sprites import LifeSprites
from pac_man.assets.sprites.sprites import MazeSprites
from pac_man.pause.pause import Pause
from pac_man.utils.enums.direction.state.ghost_state.ghost_state import GhostState
from pellets.pellets import PelletGroup
from text.text import TextGroup
from utils.enums.direction.joypad.joypad import Joypad
from utils.enums.display.character.character import Character
from utils.enums.display.display import Display
from utils.enums.display.state.executing.executing import Executing


class GameController(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pac-Man")
        self.screen = pygame.display.set_mode(Display().SCREEN_SIZE, 0, 32)
        self.clock = pygame.time.Clock()
        self.inception_maze = None
        self.maze_flash = None
        self.maze_sprites = None
        self.flash_background = None
        self.maze = None
        self.nodes = None
        self.pac_man = None
        self.pellets = None
        self.ghosts = None
        self.score = 0
        self.high_score = 0
        self.level = 0
        self.lives = 5
        self.fruit = None
        self.pause = Pause(True)
        self.text_group = TextGroup()
        self.life_sprites = LifeSprites(self.lives)
        self.fruit_array = []
        self.flash_time = 0.2
        self.flash_timer = 0
        self.maze_file_data = MazeData()
        self.maze_a_path = "maze_a.txt"
        self.maze_a_rotated_path = "maze_a_rotated.txt"

    def set_maze_background(self):
        self.inception_maze = pygame.surface.Surface(Display().SCREEN_SIZE).convert()
        self.inception_maze.fill("black")
        self.maze_flash = pygame.surface.Surface(Display().SCREEN_SIZE).convert()
        self.maze_flash.fill("black")
        self.inception_maze = self.maze_sprites.construct_maze(
            self.inception_maze, self.level % 5
        )
        self.maze_flash = self.maze_sprites.construct_maze(self.maze_flash, 5)
        self.flash_background = False
        self.maze = self.inception_maze

    def start_game(self):
        self.maze_file_data.load(self.level)
        self.maze_sprites = MazeSprites(
            self.maze_file_data.maze_object.name + ".txt",
            self.maze_file_data.maze_object.name + "_rotated.txt",
        )
        self.set_maze_background()
        self.nodes = NodeGroup(self.maze_file_data.maze_object.name + ".txt")
        self.maze_file_data.maze_object.setup_portals(self.nodes)
        self.maze_file_data.maze_object.connect_maze_legend(self.nodes)
        self.pac_man = PacMan(
            self.nodes.get_from_tiles(
                *self.maze_file_data.maze_object.pac_man_inception_node
            )
        )
        self.pellets = PelletGroup(self.maze_file_data.maze_object.name + ".txt")
        self.ghosts = GhostGroup(self.nodes.get_inception_node(), self.pac_man)

        self.ghosts.pinky.set_inception_node(
            self.nodes.get_from_tiles(*self.maze_file_data.maze_object.add_offset(2, 3))
        )
        self.ghosts.inky.set_inception_node(
            self.nodes.get_from_tiles(*self.maze_file_data.maze_object.add_offset(0, 3))
        )
        self.ghosts.clyde.set_inception_node(
            self.nodes.get_from_tiles(*self.maze_file_data.maze_object.add_offset(4, 3))
        )
        self.ghosts.set_spawn_node(
            self.nodes.get_from_tiles(*self.maze_file_data.maze_object.add_offset(2, 3))
        )
        self.ghosts.blinky.set_inception_node(
            self.nodes.get_from_tiles(*self.maze_file_data.maze_object.add_offset(2, 0))
        )
        self.nodes.deny_home_access(self.pac_man)
        self.nodes.denied_home_list(self.ghosts)
        self.ghosts.inky.inception_node.deny_access(Joypad().RIGHT, self.ghosts.inky)
        self.ghosts.clyde.inception_node.deny_access(Joypad().LEFT, self.ghosts.clyde)
        self.maze_file_data.maze_object.deny_ghosts_access(self.ghosts, self.nodes)

    def start_game_old(self):
        self.maze_file_data.load(self.level)
        self.maze_sprites = MazeSprites(self.maze_a_path, self.maze_a_rotated_path)
        self.set_maze_background()
        self.nodes = NodeGroup(self.maze_a_path)
        self.nodes.setup_portals((0, 17), (27, 17))
        legend_key = self.nodes.create_maze_legend(11.5, 14)
        self.nodes.connect_maze_legend(legend_key, (15, 14), Joypad().RIGHT)
        self.nodes.connect_maze_legend(legend_key, (12, 14), Joypad().LEFT)
        self.pac_man = PacMan(self.nodes.get_from_tiles(15, 26))
        self.pellets = PelletGroup(self.maze_a_path)
        self.ghosts = GhostGroup(self.nodes.get_inception_node(), self.pac_man)
        self.ghosts.blinky.set_inception_node(self.nodes.get_from_tiles(2 + 11.5, 0 + 14))
        self.ghosts.pinky.set_inception_node(self.nodes.get_from_tiles(2 + 11.5, 3 + 14))
        self.ghosts.inky.set_inception_node(self.nodes.get_from_tiles(0 + 11.5, 3 + 14))
        self.ghosts.clyde.set_inception_node(self.nodes.get_from_tiles(4 + 11.5, 3 + 14))
        self.ghosts.set_spawn_node(self.nodes.get_from_tiles(2 + 11.5, 3 + 14))
        self.nodes.deny_home_access(self.pac_man)
        self.nodes.denied_home_list(self.ghosts)
        self.nodes.deny_access(2 + 11.5, 3 + 14, Joypad().RIGHT, self.ghosts)
        self.nodes.deny_access(2 + 11.5, 3 + 14, Joypad().LEFT, self.ghosts)
        self.ghosts.inky.inception_node.deny_access(Joypad().RIGHT, self.ghosts.inky)
        self.ghosts.clyde.inception_node.deny_access(Joypad().LEFT, self.ghosts.clyde)
        self.nodes.denied_list(12, 14, Joypad().UP, self.ghosts)
        self.nodes.denied_list(15, 14, Joypad().UP, self.ghosts)
        self.nodes.denied_list(12, 26, Joypad().UP, self.ghosts)
        self.nodes.denied_list(15, 26, Joypad().UP, self.ghosts)

    def render(self):
        self.screen.blit(self.maze, (0, 0))
        # self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pac_man.render(self.screen)
        self.ghosts.render(self.screen)
        self.text_group.render(self.screen)

        # This loop will "'calculate' where the program needs to 'draw' the 'life sprites' 'on the 'display window:''"
        for i in range(len(self.life_sprites.life_array)):
            x = self.life_sprites.life_array[i].get_width() * i
            y = Display().SCREEN_HEIGHT - self.life_sprites.life_array[i].get_height()
            self.screen.blit(self.life_sprites.life_array[i], (x, y))

        for i in range(len(self.fruit_array)):
            x = Display().SCREEN_WIDTH - self.fruit_array[i].get_width() * (i + 1)
            y = Display().SCREEN_HEIGHT - self.fruit_array[i].get_height()
            self.screen.blit(self.fruit_array[i], (x, y))
        pygame.display.update()

    def show_entities(self):
        self.pac_man.visible = True
        self.ghosts.show()

    def check_keydown_events(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN and self.pac_man.alive:
                    self.pause.set_pause(pause=True)
                    if not self.pause.paused:
                        self.text_group.hide_text()
                        self.show_entities()
                    else:
                        self.text_group.show_text(Executing().PAUSE_TEXT)
                elif event.key == K_ESCAPE:
                    exit()
            elif event.type == QUIT:
                exit()

    def check_pellet_events(self):
        pellet = self.pac_man.devour_pellet(self.pellets.pellet_array)
        if pellet:
            self.pellets.number_eaten += 1
            self.update_scores(pellet.points)
            if self.pellets.number_eaten == 30:
                self.ghosts.inky.inception_node.grant_access(
                    Joypad().RIGHT, self.ghosts.inky
                )
            if self.pellets.number_eaten == 70:
                self.ghosts.clyde.inception_node.grant_access(
                    Joypad().LEFT, self.ghosts.clyde
                )
            self.pellets.pellet_array.remove(pellet)
            if pellet.name == Character().POWER_PELLET:
                self.ghosts.initial_fright_state()
            if self.pellets.empty():
                self.flash_background = True
                self.hide_entities()
                # "Pause" the game for "'3s' ''after' 'pac-man' has ''finished' 'eating'' ''all' the 'pellets''' and 'before'
                # the 'next level:''"
                self.pause.set_pause(pause_time=3, function=self.next_level)

    def check_ghost_events(self):
        for ghost in self.ghosts:
            if self.pac_man.collide_with_ghost(ghost):
                if ghost.mode.current is GhostState().FRIGHTENED:
                    self.pac_man.visible = False
                    ghost.visible = False
                    self.update_scores(ghost.points)
                    self.text_group.add_text(
                        str(ghost.points),
                        "white",
                        ghost.position.x,
                        ghost.position.y,
                        8,
                        time=1,
                    )
                    self.ghosts.update_points()
                    # "Pause" the game for "'1s' ''after' a 'ghost' has been 'eaten:''"
                    self.pause.set_pause(pause_time=1, function=self.show_entities)
                    ghost.initial_spawn_state()
                    self.nodes.grant_home_access(ghost)
                elif ghost.mode.current is not GhostState().SPAWN:
                    if self.pac_man.alive:
                        self.lives -= 1
                        self.life_sprites.remove_sprite()
                        self.pac_man.died()
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.text_group.show_text(Executing().GAME_OVER_TEXT)
                            # "Pause" the game for "'3s' ''after' 'pac-man' has 'died'' and 'before' ''restarting' the game's level:''"
                            self.pause.set_pause(pause_time=3, function=self.restart_game)
                        else:
                            # "Pause" the game for "'3s' ''after' 'pac-man' has 'died'' and 'before' ''resetting' the game's level:''"
                            self.pause.set_pause(pause_time=3, function=self.reset_level)

    def check_fruit_events(self):
        if self.pellets.number_eaten == 50 or self.pellets.number_eaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.get_from_tiles(9, 20), self.level)
                print(self.fruit)
        if self.fruit is not None:
            if self.pac_man.collision_type(self.fruit):
                self.update_scores(self.fruit.points)
                self.text_group.add_text(
                    str(self.fruit.points),
                    "white",
                    self.fruit.position.x,
                    self.fruit.position.y,
                    8,
                    time=1,
                )
                fruit_eaten = False
                for fruit in self.fruit_array:
                    if fruit.get_offset() == self.fruit.sprite.get_offset():
                        fruit_eaten = True
                        break
                if not fruit_eaten:
                    self.fruit_array.append(self.fruit.sprite)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def hide_entities(self):
        self.pac_man.visible = False
        self.ghosts.hide()

    def next_level(self):
        self.show_entities()
        self.level += 1
        self.pause.paused = True
        self.start_game()
        self.text_group.update_level(self.level)
        self.text_group.show_text(Executing().READY_TEXT)

    def restart_game(self):
        self.level = 0
        self.lives = 5
        self.pause.paused = True
        self.fruit = None
        self.start_game()
        self.score = 0
        self.text_group.update_score(self.score)
        self.text_group.update_level(self.level)
        self.text_group.show_text(Executing().READY_TEXT)
        self.life_sprites.reset_lives(self.lives)
        self.fruit_array = []

    def reset_level(self):
        self.pause.paused = True
        self.pac_man.reset()
        self.ghosts.reset()
        self.fruit = None
        self.text_group.show_text(Executing().READY_TEXT)

    def update_scores(self, points):
        self.score += points
        self.text_group.update_score(self.score)
        self.high_score = self.score
        self.text_group.update_high_score(self.high_score)

    def update(self):
        dt = self.clock.tick(360) / 1000
        self.text_group.update(dt)
        self.pellets.update(dt)
        if not self.pause.paused:
            self.ghosts.update(dt)
            if self.fruit is not None:
                self.fruit.update_existence_timer(dt)
            self.check_pellet_events()
            self.check_ghost_events()
            self.check_fruit_events()
        if self.pac_man.alive:
            if not self.pause.paused:
                self.pac_man.update(dt)
        else:
            self.pac_man.update(dt)
        if self.flash_background:
            self.flash_timer += dt
            if self.flash_timer >= self.flash_time:
                self.flash_timer = 0
                if self.maze == self.inception_maze:
                    self.maze = self.maze_flash
                else:
                    self.maze = self.inception_maze
        pause_state = self.pause.update(dt)
        if pause_state is not None:
            pause_state()
        self.check_keydown_events()
        self.render()


if __name__ == "__main__":
    game = GameController()
    game.start_game()
    while True:
        game.update()
