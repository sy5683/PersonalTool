from ...entity.types import Types


class Fairy(Types):

    def __init__(self):
        super().__init__("fairy")
        self.fire = 0.5
        self.fighting = 2
        self.poison = 0.5
        self.dragon = 2
        self.dark = 2
        self.steel = 0.5
