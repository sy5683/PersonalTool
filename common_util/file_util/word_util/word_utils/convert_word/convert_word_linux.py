import typing
from pathlib import Path

from .convert_word import ConvertWord


class ConvertWordLinux(ConvertWord):

    @classmethod
    def word_to_pdf(cls, word_path: str, save_path: typing.Union[Path, str]) -> str:
        """word转pdf"""
        raise FileExistsError("暂不支持的转换功能。")