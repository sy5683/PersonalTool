import re
import typing
from urllib import parse
from enum import Enum


class DecodeType(Enum):
    unicode = "unicode"
    utf_8 = "utf_8"

class ConvertTextual:

    @classmethod
    def textual_decode(cls, textual: typing.Union[bytes, str]) -> str:
        """文本解码"""
        # 1) 格式化文本
        textual = cls._format_textual(textual)
        # 2) 判断文本转码类型
        decode_types = []
        if re.search(r"\\u", textual):
            decode_types.append(DecodeType.unicode)
        if re.match(r"\\x", textual):
            decode_types.append(DecodeType.utf_8)
        # 3) 根据文本类型转码
        if len(decode_types) > 1:
            raise TypeError("文本异常，有多种格式的转码类型，无法解析")
        elif decode_types == [DecodeType.unicode]:
            return cls._unicode_to_str(textual)
        elif decode_types == [DecodeType.utf_8]:
            return cls._utf_8_to_str(textual)
        else:
            raise TypeError("暂不支持的文本解码类型")

    @staticmethod
    def _format_textual(textual: typing.Union[bytes, str]) -> str:
        """格式化文本"""
        # 1) bytes类型转码为字符串
        if isinstance(textual, bytes):
            textual = textual.decode()
        # 2) 将文本中的单斜杠统一转换为双斜杠
        return textual.encode("raw_unicode_escape").decode()

    @staticmethod
    def _unicode_to_str(unicodes: str) -> str:
        """unicode转字符串"""
        # 1) 接收的unicode中特殊字符可能会出现不足四位的情况，因此使用正则表达式在其前方补零
        for unicode in list(set(re.findall(r"(\\u\w{1,3})(?=[\\<])", unicodes))):
            code = unicode.replace("\\u", "")
            unicodes = unicodes.replace(unicode, unicode.replace(f"\\u{code}", f"\\u{code.zfill(4)}"))
        # 2) 特殊处理一些无法在xmltodict方法中使用的字符串
        # 正则批量去除无法解码的字符串
        unicodes = re.sub(r"\\u0000", "", unicodes)
        # 【<】无法使用，替换为【《】（【>】可以使用，但是为了美观，也替换为【》】）
        unicodes = unicodes.replace("\\u003c", "\\u300a").replace("\\u003e", "\\u300b")
        return unicodes.encode('utf-8').decode('unicode_escape')

    @staticmethod
    def _utf_8_to_str(utf_8: str) -> str:
        """utf-8转字符串"""
        return parse.unquote(utf_8.replace("\\x", "%"))
