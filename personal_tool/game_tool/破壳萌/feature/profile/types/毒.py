from ...entity.types import Types


class Poison(Types):

    def __init__(self):
        super().__init__("poison")
        self.grass = 2
        self.poison = 0.5
        self.ground = 0.5
        self.rock = 0.5
        self.ghost = 0.5
        self.steel = 0
        self.fairy = 2
