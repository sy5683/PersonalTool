import typing

from .textual_utils.convert_chinese import ConvertChinese
from .textual_utils.convert_textual import ConvertTextual
from .textual_utils.process_chinese import ProcessChinese


class TextualUtil:

    @staticmethod
    def chinese_to_object_name(chinese: str) -> str:
        """中文转对象名"""
        return ConvertChinese.chinese_to_object_name(chinese)

    @staticmethod
    def textual_decode(textual: typing.Union[bytes, str]) -> str:
        """文本解码"""
        return ConvertTextual.textual_decode(textual)

    @staticmethod
    def spilt_address(address: str) -> typing.Tuple[str, str, str, str]:
        """将地址分割为省、市、区、地址"""
        return ProcessChinese.spilt_address(address)

