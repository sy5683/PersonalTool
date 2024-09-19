from ...entity.types import Types


class Water(Types):

    def __init__(self):
        super().__init__("water")
        self.fire = 2
        self.water = 0.5
        self.grass = 0.5
        self.ground = 2
        self.rock = 2
        self.dragon = 0.5
