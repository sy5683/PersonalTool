from ...entity.types import Types


class Psychic(Types):

    def __init__(self):
        super().__init__("psychic")
        self.fighting = 2
        self.poison = 2
        self.psychic = 0.5
        self.dark = 0
        self.steel = 0.5
