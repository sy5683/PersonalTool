import abc


class Types(metaclass=abc.ABCMeta):

    def __init__(self, name: str = ''):
        self.name = name
        self.normal = 1  # 一般
        self.fire = 1  # 火
        self.water = 1  # 水
        self.grass = 1  # 草
        self.electric = 1  # 电
        self.ice = 1  # 冰
        self.fighting = 1  # 格斗
        self.poison = 1  # 毒
        self.ground = 1  # 地面
        self.fly = 1  # 飞行
        self.psychic = 1  # 超能
        self.bug = 1  # 虫
        self.rock = 1  # 岩
        self.ghost = 1  # 幽灵
        self.dragon = 1  # 龙
        self.dark = 1  # 恶
        self.steel = 1  # 钢
        self.fairy = 1  # 妖精

    def __str__(self) -> str:
        return self.name
