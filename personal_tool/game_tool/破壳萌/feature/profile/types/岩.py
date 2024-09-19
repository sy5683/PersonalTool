from ...entity.types import Types


class Rock(Types):

    def __init__(self):
        super().__init__("rock")
        self.fire = 2
        self.ice = 2
        self.fighting = 0.5
        self.ground = 0.5
        self.fly = 2
        self.bug = 2
        self.steel = 0.5
