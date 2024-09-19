from ...entity.types import Types


class Dark(Types):

    def __init__(self):
        super().__init__("dark")
        self.fighting = 0.5
        self.psychic = 2
        self.ghost = 2
        self.dark = 0.5
        self.fairy = 0.5
