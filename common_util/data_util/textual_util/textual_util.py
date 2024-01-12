import typing

from .textual_utils.convert_chinese import ConvertChinese
from .textual_utils.convert_textual import ConvertTextual


class TextualUtil:

    @staticmethod
    def chinese_to_object_name(chinese: str) -> str:
        """中文转对象名"""
        return ConvertChinese.chinese_to_object_name(chinese)

    @staticmethod
    def textual_decode(textual: typing.Union[bytes, str]) -> str:
        """文本解码"""
        return ConvertTextual.textual_decode(textual)
