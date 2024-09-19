from ...entity.types import Types


class Fighting(Types):

    def __init__(self):
        super().__init__("fighting")
        self.normal = 2
        self.ice = 2
        self.poison = 0.5
        self.fly = 0.5
        self.psychic = 0.5
        self.bug = 0.5
        self.rock = 2
        self.ghost = 0
        self.dark = 2
        self.steel = 2
        self.fairy = 0.5
