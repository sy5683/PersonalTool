from ...entity.monster import Monster


class N0001(Monster):

    def __init__(self):
        super().__init__(1, "妙蛙种子")
        self.types = []
        self.HP = 45
        self.ATK = 49
        self.DEF = 49
        self.SPA = 65
        self.SPD = 65
        self.SPE = 45
