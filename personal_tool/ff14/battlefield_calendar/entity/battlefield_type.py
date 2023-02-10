from enum import Enum


class BattlefieldType(Enum):
    zd = {'sign': "阵地", 'index': 0, 'name': "阵地"}
    cf = {'sign': "尘封", 'index': 1, 'name': "尘封秘岩争夺战"}
    sb = {'sign': "碎冰", 'index': 2, 'name': "碎冰"}
    cy = {'sign': "草原", 'index': 3, 'name': "昂撒哈凯尔竞争战"}

    def to_sign(self) -> str:
        return self.value['sign']

    def to_index(self) -> int:
        return self.value['index']

    @classmethod
    def get_enum_by_index(cls, value: int, revision: int):
        index = (value + revision) % len(BattlefieldType)
        for member in cls:
            if member.value['index'] == index:
                return member
