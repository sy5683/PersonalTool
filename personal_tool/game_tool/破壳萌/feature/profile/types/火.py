from ...entity.types import Types


class Fire(Types):

    def __init__(self):
        super().__init__("fire")
        self.fire = 0.5
        self.water = 0.5
        self.grass = 2
        self.ice = 2
        self.bug = 2
        self.rock = 0.5
        self.dragon = 0.5
        self.steel = 2
