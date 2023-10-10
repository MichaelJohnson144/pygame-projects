from py_man.assets.sprites.sprites import FruitSprites
from py_man.entity.entity import Entity
from py_man.utils.enums.direction.joypad.joypad import JoyPad
from py_man.utils.enums.display.character.character import Character


class Fruit(Entity):
    def __init__(self, node, level=0):
        super().__init__(node)
        self.name = Character().FRUIT
        self.color = "green"
        self.timer = 0
        self.lifespan = 5
        self.destroy = False
        self.points = 100 + (level * 20)
        self.set_entity_between_nodes(JoyPad().RIGHT)
        self.sprites = FruitSprites(self, level)

    def update_existence_timer(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True
