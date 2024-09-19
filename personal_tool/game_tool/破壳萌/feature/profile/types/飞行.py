from ...entity.types import Types


class Fly(Types):

    def __init__(self):
        super().__init__("fly")
        self.grass = 2
        self.electric = 0.5
        self.fighting = 2
        self.bug = 2
        self.rock = 0.5
        self.steel = 0.5
