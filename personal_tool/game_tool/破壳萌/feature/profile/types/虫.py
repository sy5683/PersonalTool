from ...entity.types import Types


class Bug(Types):

    def __init__(self):
        super().__init__("bug")
        self.fire = 0.5
        self.grass = 2
        self.fighting = 0.5
        self.poison = 0.5
        self.fly = 0.5
        self.psychic = 2
        self.ghost = 0.5
        self.dark = 2
        self.steel = 0.5
        self.fairy = 0.5
