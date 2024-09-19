class Monster:

    def __init__(self, code: int, name: str):
        self.code = code  # 编号
        self.name = name  # 名称
        self.types = []  # 属性
        """种族值"""
        self.HP = 0  # 血量
        self.ATK = 0  # 物攻
        self.DEF = 0  # 物防
        self.SPA = 0  # 特攻
        self.SPD = 0  # 特防
        self.SPE = 0  # 速度
        """努力值"""

    def __str__(self) -> str:
        return f"{self.code}.{self.name}"

    @property
    def IV(self) -> int:
        """种族值"""
        return self.HP + self.ATK + self.DEF + self.SPA + self.SPD + self.SPE
