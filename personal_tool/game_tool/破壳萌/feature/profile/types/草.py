from ...entity.types import Types


class Grass(Types):

    def __init__(self):
        super().__init__("grass")
        self.fire = 0.5
        self.water = 2
        self.grass = 0.5
        self.poison = 0.5
        self.ground = 2
        self.fly = 0.5
        self.bug = 0.5
        self.rock = 2
        self.dragon = 0.5
        self.steel = 0.5
