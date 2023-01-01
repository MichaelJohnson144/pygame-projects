from pac_man.assets.sprites.sprites import FruitSprites
from pac_man.entity.entity import Entity
from pac_man.utils.enums.direction.joypad.joypad import Joypad
from pac_man.utils.enums.display.character.character import Character


class Fruit(Entity):
    def __init__(self, node, level=0):
        Entity.__init__(self, node)
        self.name = Character().FRUIT
        self.color = "green"
        self.timer = 0
        # The "fruit" will "'disappear' ''after' '5s'' ''if' Pac-Man ''fails' to ''eat it' 'before then:''''"
        self.lifespan = 5
        self.destroy = False
        self.points = 100 + (level * 20)
        self.set_entity_between_nodes(Joypad().RIGHT)
        self.sprites = FruitSprites(self, level)

    def update_existence_timer(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True
