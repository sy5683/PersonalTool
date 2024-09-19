from ...entity.types import Types


class Steel(Types):

    def __init__(self):
        super().__init__("steel")
        self.fire = 0.5
        self.water = 0.5
        self.electric = 0.5
        self.ice = 2
        self.rock = 2
        self.steel = 0.5
        self.fairy = 2
