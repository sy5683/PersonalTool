from ...entity.types import Types


class Electric(Types):

    def __init__(self):
        super().__init__("electric")
        self.water = 2
        self.grass = 0.5
        self.electric = 0.5
        self.ground = 0
        self.fly = 2
        self.dragon = 0.5
