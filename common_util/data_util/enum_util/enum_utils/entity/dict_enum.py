from enum import Enum


class DictEnum(Enum):

    def __init_subclass__(cls):
        for member in cls:
            # 校验枚举对象是否均为字典
            assert isinstance(member.value, dict)

    def _to_value(self, key: str):
        return self.value[key]

    @classmethod
    def _get_by_key(cls, key: str, value: str):
        for member in cls:
            if member._to_value(key) == value:
                return member
        raise ValueError(f"【{cls}】中未找到指定值为【{value}】的键: {key}")
