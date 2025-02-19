from common_util.data_util.enum_util.enum_utils.entity.dict_enum import DictEnum


class ColorMap(DictEnum):
    black = {'code': "H", 'name': "黑"}
    red = {'code': "R", 'name': "红"}
    blue = {'code': "B", 'name': "蓝"}
    yellow = {'code': "Y", 'name': "黄"}

    def to_code(self) -> str:
        return self._to_value("code")

    def to_name(self) -> str:
        return self._to_value("name")

    @classmethod
    def code_to_name(cls, color_code: str) -> str:
        for enum in cls:
            if color_code == enum.to_code():
                return enum.to_name()
            if color_code == enum.to_name():
                return color_code
        raise ValueError(f"未知的异常颜色数据: {color_code}")
