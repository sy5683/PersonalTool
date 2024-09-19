from ...entity.types import Types


class Normal(Types):

    def __init__(self):
        super().__init__("normal")
        self.rock = 0.5
        self.ghost = 0
        self.steel = 0.5
