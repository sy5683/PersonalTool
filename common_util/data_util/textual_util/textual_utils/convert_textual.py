import re
import typing
from urllib import parse


class ConvertTextual:

    @classmethod
    def textual_decode(cls, textual: typing.Union[bytes, str]) -> str:
        """文本解码"""
        # 1) 格式化文本
        textual = cls._format_textual(textual)
        # 2) 根据文本类型转码
        if re.match(r"\\u", textual):
            return cls._unicode_to_str(textual)
        elif re.match(r"\\x", textual):
            return cls._utf_8_to_str(textual)
        else:
            return textual

    @staticmethod
    def _format_textual(textual: typing.Union[bytes, str]) -> str:
        """格式化文本"""
        # bytes
        if isinstance(textual, bytes):
            textual = textual.decode()
        return textual.encode("raw_unicode_escape").decode()

    @staticmethod
    def _unicode_to_str(unicodes: str) -> str:
        """unicode转字符串"""
        # 接收的unicode中特殊字符可能会出现不足四位的情况，因此使用正则表达式在其前方补零
        for unicode in re.findall(r"(\\u\w{1,3})(?=[\\<])", unicodes):
            code = unicode.replace("\\u", "")
            unicodes = unicodes.replace(unicode, unicode.replace(f"\\u{code}", f"\\u{code.zfill(4)}"))
        return unicodes.encode('utf-8').decode('unicode_escape')

    @staticmethod
    def _utf_8_to_str(utf_8: str) -> str:
        """utf-8转字符串"""
        return parse.unquote(utf_8.replace("\\x", "%"))
