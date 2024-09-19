from ...entity.types import Types


class Ice(Types):

    def __init__(self):
        super().__init__("ice")
        self.fire = 0.5
        self.water = 0.5
        self.grass = 2
        self.ice = 0.5
        self.ground = 2
        self.fly = 2
        self.dragon = 2
        self.steel = 0.5
