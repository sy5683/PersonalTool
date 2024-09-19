from ...entity.types import Types


class Ground(Types):

    def __init__(self):
        super().__init__("ground")
        self.fire = 2
        self.grass = 0.5
        self.electric = 2
        self.poison = 2
        self.fly = 0
        self.bug = 0.5
        self.rock = 2
        self.steel = 2
