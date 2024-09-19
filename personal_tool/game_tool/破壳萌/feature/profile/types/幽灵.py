from ...entity.types import Types


class Ghost(Types):

    def __init__(self):
        super().__init__("ghost")
        self.psychic = 2
        self.ghost = 2
        self.dark = 0.5
