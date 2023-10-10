import pygame
from pygame.locals import KEYDOWN, K_RETURN, K_ESCAPE, QUIT

from maze_data.maze_data import MazeData
from nodes.nodes import NodeGroup
from pellets.pellets import PelletGroup
from py_man.assets.sprites.characters.ghosts import GhostGroup
from py_man.assets.sprites.characters.py_man import PyMan
from py_man.assets.sprites.fruit.fruit import Fruit
from py_man.assets.sprites.sprites import LifeSprites
from py_man.assets.sprites.sprites import MazeSprites
from py_man.pause.pause import Pause
from py_man.utils.enums.direction.state.ghost_state.ghost_state import GhostState
from text.text import TextGroup
from utils.enums.direction.joypad.joypad import JoyPad
from utils.enums.display.character.character import Character
from utils.enums.display.display import Display
from utils.enums.display.state.executing.executing import Executing


class EventHandlers(object):
    def __init__(self):
        pygame.init()
        self.display = Display()
        pygame.display.set_caption("Py-Man")
        self.screen = pygame.display.set_mode(
            (self.display.SCREEN_WIDTH, self.display.SCREEN_HEIGHT),
            pygame.DOUBLEBUF | pygame.HWSURFACE,
        )
        self.clock = pygame.time.Clock()
        self.inception_maze = None
        self.flashy_maze = None
        self.maze_sprites = None
        self.flashy_background = None
        self.maze = None
        self.nodes = None
        self.py_man = None
        self.pellets = None
        self.joypad = JoyPad()
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
        self.executing = Executing()
        self.maze_a_path = "maze_a.txt"
        self.maze_a_rotated_path = "maze_a_rotated.txt"


class InitialEvents(EventHandlers):
    def __init__(self):
        super().__init__()

    def set_maze_background(self):
        maze_size = self.display.SCREEN_SIZE
        self.inception_maze, self.flashy_maze = [
            self.maze_sprites.construct_maze(pygame.Surface(maze_size).convert(), i)
            for i in (self.level % 5, 5)
        ]
        self.flashy_background = False
        self.maze = self.inception_maze

    def load_maze_data_from_file(self):
        self.maze_file_data.load(self.level)

    def initialize_maze_sprites(self):
        maze_name = self.maze_file_data.maze_object.name
        self.maze_sprites = MazeSprites(f"{maze_name}.txt", f"{maze_name}_rotated.txt")
        self.set_maze_background()

    def initialize_maze_nodes(self):
        maze_nodes_file = f"{self.maze_file_data.maze_object.name}.txt"
        self.nodes = NodeGroup(maze_nodes_file)
        self.maze_file_data.maze_object.connect_portals(self.nodes)
        self.maze_file_data.maze_object.link_vertically(self.nodes)

    def initialize_py_man_and_pellets(self):
        py_man_node = self.nodes.retrieve_from_tile_coordinates(
            *self.maze_file_data.maze_object.py_man_inception_node
        )
        self.py_man = PyMan(py_man_node)
        self.pellets = PelletGroup(f"{self.maze_file_data.maze_object.name}.txt")

    def initialize_ghosts(self):
        ghost_positions = [
            ((2, 3), "pinky"),
            ((0, 3), "inky"),
            ((4, 3), "clyde"),
            ((2, 0), "blinky"),
        ]
        self.ghosts = GhostGroup(self.nodes.get_inception_node(), self.py_man)
        ghost_map = {
            "pinky": self.ghosts.pinky,
            "inky": self.ghosts.inky,
            "clyde": self.ghosts.clyde,
            "blinky": self.ghosts.blinky,
        }
        for position, name in ghost_positions:
            ghost = ghost_map[name]
            ghost.set_inception_node(
                self.nodes.retrieve_from_tile_coordinates(
                    *self.maze_file_data.maze_object.add_offset(*position)
                )
            )
            if name == "pinky":
                self.ghosts.set_spawn_point(
                    self.nodes.retrieve_from_tile_coordinates(
                        *self.maze_file_data.maze_object.add_offset(*position)
                    )
                )

    def restrict_py_man_movement(self):
        self.nodes.block_spawn_point_movements(self.py_man)

    def restrict_ghost_movement(self):
        self.nodes.block_spawn_point_movements_for_entities(self.ghosts)
        self.ghosts.inky.inception_node.block_direction(
            self.joypad.RIGHT, self.ghosts.inky
        )
        self.ghosts.clyde.inception_node.block_direction(
            self.joypad.LEFT, self.ghosts.clyde
        )

    def restrict_ghost_movement_in_maze(self):
        self.maze_file_data.maze_object.block_access(self.ghosts, self.nodes)

    def start_game(self):
        self.load_maze_data_from_file()
        self.initialize_maze_sprites()
        self.initialize_maze_nodes()
        self.initialize_py_man_and_pellets()
        self.initialize_ghosts()
        self.restrict_py_man_movement()
        self.restrict_ghost_movement()
        self.restrict_ghost_movement_in_maze()


class RenderEvents(InitialEvents):
    def __init__(self):
        super().__init__()

    def render_maze(self):
        self.screen.blit(self.maze, (0, 0))

    def render_sprites(self):
        screen = self.screen
        self.pellets.render(screen)
        if self.fruit:
            self.fruit.render(screen)
        self.py_man.render(screen)
        self.ghosts.render(screen)
        self.text_group.render(screen)

    def render_lives(self):
        life_sprites = self.life_sprites.life_array
        if not life_sprites:
            return
        life_width, life_height = life_sprites[0].get_size()
        for i, life_sprite in enumerate(life_sprites):
            self.screen.blit(
                life_sprite, (life_width * i, self.display.SCREEN_HEIGHT - life_height)
            )

    def render_fruits(self):
        if not self.fruit_array:
            return
        fruit_width, fruit_height = self.fruit_array[0].get_size()
        x = self.display.SCREEN_WIDTH - fruit_width
        y = self.display.SCREEN_HEIGHT - fruit_height
        self.screen.blit(self.fruit_array[0], (x, y))
        for fruit_sprite in self.fruit_array[1:]:
            fruit_width, fruit_height = fruit_sprite.get_size()
            x -= fruit_width
            self.screen.blit(fruit_sprite, (x, y))
        pygame.display.update()

    def render(self):
        self.render_maze()
        self.render_sprites()
        self.render_lives()
        self.render_fruits()
        pygame.display.flip()

    def show_entities(self):
        self.py_man.visible = True
        self.ghosts.show()

    def hide_entities(self):
        self.py_man.visible = False
        self.ghosts.hide()


class ExecutionEvents(RenderEvents):
    def __init__(self):
        super().__init__()

    def next_level(self):
        self.show_entities()
        self.level += 1
        self.pause.paused = True
        self.start_game()
        self.text_group.update_level(self.level)
        self.text_group.show_text(self.executing.READY_TEXT)

    def restart_game(self):
        self.level = 0
        self.lives = 5
        self.pause.paused = True
        self.fruit = None
        self.start_game()
        self.score = 0
        self.text_group.update_score(self.score)
        self.text_group.update_level(self.level)
        self.text_group.show_text(self.executing.READY_TEXT)
        self.life_sprites.reset_lives(self.lives)
        self.fruit_array = []

    def reset_level(self):
        self.pause.paused = True
        self.py_man.reset()
        self.ghosts.reset()
        self.fruit = None
        self.text_group.show_text(self.executing.READY_TEXT)

    def update_scores(self, points):
        self.score += int(points)
        self.text_group.update_score(self.score)
        self.high_score = self.score
        self.text_group.update_high_score(self.high_score)


class RestartEvents(RenderEvents):
    def __init__(self):
        super().__init__()

    def load_maze_file_data(self):
        self.maze_file_data.load(self.level)

    def initialize_maze_sprites(self):
        self.maze_sprites = MazeSprites(self.maze_a_path, self.maze_a_rotated_path)
        self.set_maze_background()

    def initialize_maze_nodes(self):
        self.nodes = NodeGroup(self.maze_a_path)
        self.nodes.connect_portals((0, 17), (27, 17))

    def connect_nodes_to_legend(self, legend_key, connect_list):
        for connect in connect_list:
            self.nodes.link_spawn_point_layout(legend_key, *connect)

    def initialize_maze_legend(self):
        legend_key = self.nodes.generate_spawn_point_layout(11.5, 14)
        legend_connect_list = [(15, 14, self.joypad.RIGHT), (12, 14, self.joypad.LEFT)]
        self.connect_nodes_to_legend(legend_key, legend_connect_list)

    def initialize_py_man(self):
        self.py_man = PyMan(self.nodes.retrieve_from_tile_coordinates(15, 26))
        self.nodes.block_spawn_point_movements(self.py_man)

    def initialize_pellets(self):
        self.pellets = PelletGroup(self.maze_a_path)

    def deny_access_to_node(self, position, direction, ghost):
        self.nodes.block_direction(*position, ghost, direction=direction)

    def initialize_ghosts(self):
        self.ghosts = GhostGroup(self.nodes.get_inception_node(), self.py_man)
        self.ghosts.set_spawn_point(
            self.nodes.retrieve_from_tile_coordinates(2 + 11.5, 3 + 14)
        )
        restricted_home_ghosts = [self.ghosts]
        restricted_positions_and_directions_nodes = [
            ((2 + 11.5, 3 + 14), self.joypad.RIGHT),
            ((2 + 11.5, 3 + 14), self.joypad.LEFT),
        ]
        restricted_positions_and_directions = [
            ((12, 14), self.joypad.UP),
            ((15, 14), self.joypad.UP),
            ((12, 26), self.joypad.UP),
            ((15, 26), self.joypad.UP),
        ]
        [
            self.nodes.block_spawn_point_movements_for_entities(ghost)
            for ghost in restricted_home_ghosts
        ]
        [
            self.deny_access_to_node(position, direction, self.ghosts)
            for position, direction in restricted_positions_and_directions_nodes
        ]
        [
            self.deny_access_to_node(position, direction, self.ghosts)
            for position, direction in restricted_positions_and_directions
        ]
        ghost_connect_list = [
            (self.ghosts.blinky, (2 + 11.5, 0 + 14)),
            (self.ghosts.pinky, (2 + 11.5, 3 + 14)),
            (self.ghosts.inky, (0 + 11.5, 3 + 14), self.joypad.RIGHT),
            (self.ghosts.clyde, (4 + 11.5, 3 + 14), self.joypad.LEFT),
        ]
        for ghost, position, direction in ghost_connect_list:
            ghost.set_inception_node(self.nodes.retrieve_from_tile_coordinates(*position))
            if ghost == self.ghosts.inky:
                ghost.inception_node.block_direction(direction, ghost)


class KeyDownEvents(RenderEvents):
    def __init__(self):
        super().__init__()

    def handle_keydown_events(self):
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            if (event.key, self.py_man.alive) == (K_RETURN, True):
                self.pause.set_pause(pause=True)
                (
                    self.text_group.show_text(self.executing.PAUSE_TEXT)
                    if self.pause.paused
                    else self.text_group.hide_text() or self.show_entities()
                )
            elif event.key == K_ESCAPE:
                exit()
        elif event.type == QUIT:
            exit()


class PelletEvents(ExecutionEvents):
    def __init__(self):
        super().__init__()

    def release_ghost(self, ghost):
        direction = self.joypad.LEFT if ghost == self.ghosts.clyde else self.joypad.RIGHT
        ghost.inception_node.allow_direction(direction, ghost)

    def remove_pellet(self, pellet):
        self.pellets.pellet_array.remove(pellet)

    def handle_power_pellet(self, pellet):
        if pellet.name == Character().POWER_PELLET:
            self.ghosts.frightened()

    def handle_pellet_completion(self):
        if self.pellets.empty():
            self.flashy_background = True
            self.hide_entities()
            self.pause.set_pause(pause_time=3, function=self.next_level)

    def handle_pellet_events(self):
        pellet = self.py_man.devour_pellet(self.pellets.pellet_array)
        if not pellet:
            return
        self.pellets.number_eaten += 1
        self.update_scores(pellet.points)
        if self.pellets.number_eaten in {30, 70}:
            ghost = (
                self.ghosts.inky if self.pellets.number_eaten == 30 else self.ghosts.clyde
            )
            self.release_ghost(ghost)
        self.remove_pellet(pellet)
        self.handle_power_pellet(pellet)
        self.handle_pellet_completion()


class GhostEvents(ExecutionEvents):
    def __init__(self):
        super().__init__()

    def handle_frightened_ghost(self, ghost):
        self.py_man.visible = ghost.visible = False
        points = str(ghost.points)
        self.update_scores(points)
        self.text_group.add_text(
            points, "white", ghost.position.x, ghost.position.y, 8, time=1
        )
        self.ghosts.update_points()
        self.pause.set_pause(pause_time=1, function=self.show_entities)
        ghost.initial_spawn_state()
        self.nodes.allow_spawn_point_movements(ghost)

    def handle_game_over(self):
        game_over_text = self.executing.GAME_OVER_TEXT
        self.text_group.show_text(game_over_text)
        self.pause.set_pause(pause_time=3, function=self.restart_game)

    def handle_reset_level(self):
        self.pause.set_pause(pause_time=3, function=self.reset_level)

    def handle_live_ghost(self, _):
        self.lives -= 1
        self.life_sprites.remove_sprite()
        self.py_man.died()
        self.ghosts.hide()
        if self.lives <= 0:
            self.handle_game_over()
        else:
            self.handle_reset_level()

    def handle_ghost_events(self):
        frightened = GhostState().FRIGHTENED
        spawn = GhostState().SPAWN
        for ghost in self.ghosts:
            if not self.py_man.collide_with_ghost(ghost):
                continue
            if ghost.state_controller.current == frightened:
                self.handle_frightened_ghost(ghost)
            elif ghost.state_controller.current != spawn and self.py_man.alive:
                self.handle_live_ghost(ghost)


class FruitEvents(ExecutionEvents):
    def __init__(self):
        super().__init__()

    def spawn_fruit(self):
        if self.pellets.number_eaten in {50, 140}:
            self.fruit = Fruit(
                self.nodes.retrieve_from_tile_coordinates(9, 20), self.level
            )

    def add_fruit_to_array(self):
        fruit_offset = self.fruit.sprite.get_offset()
        if fruit_offset not in [fruit.get_offset() for fruit in self.fruit_array]:
            self.fruit_array.append(self.fruit.sprite)

    def handle_fruit_collision(self):
        if self.fruit and self.py_man.collision_type(self.fruit):
            self.update_scores(self.fruit.points)
            self.text_group.add_text(
                str(self.fruit.points),
                "white",
                self.fruit.position.x,
                self.fruit.position.y,
                8,
                time=1,
            )
            self.add_fruit_to_array()
            self.fruit = None
        elif self.fruit and self.fruit.destroy:
            self.fruit = None

    def handle_fruit_events(self):
        self.spawn_fruit()
        self.handle_fruit_collision()


class UpdateEvent(KeyDownEvents, PelletEvents, GhostEvents, FruitEvents):
    def __init__(self):
        super().__init__()

    def update(self):
        dt = self.clock.tick(360) / 1000
        self.text_group.update(dt)
        self.pellets.update(dt)
        if not self.pause.paused:
            self.ghosts.update(dt)
            if self.fruit is not None:
                self.fruit.update_existence_timer(dt)
            self.handle_pellet_events()
            self.handle_ghost_events()
            self.handle_fruit_events()
        if self.py_man.alive:
            if not self.pause.paused:
                self.py_man.update(dt)
        else:
            self.py_man.update(dt)
        if self.flashy_background:
            self.flash_timer += dt
            if self.flash_timer >= self.flash_time:
                self.flash_timer = 0
                if self.maze == self.inception_maze:
                    self.maze = self.flashy_maze
                else:
                    self.maze = self.inception_maze
        pause_state = self.pause.update(dt)
        if pause_state is not None:
            pause_state()
        self.handle_keydown_events()
        self.render()


if __name__ == "__main__":
    game = InitialEvents() and UpdateEvent()
    game.start_game()
    while True:
        game.update()
