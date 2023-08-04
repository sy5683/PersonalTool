from pathlib import Path
from typing import Union


class TxtUtil:
    _encoding_type = "UTF-8"  # 编码格式统一为UTF-8

    @classmethod
    def txt_read(cls, txt_path: Union[str, Path]) -> str:
        """读取txt文件中的内容"""
        with open(str(txt_path), "r", encoding=cls._encoding_type) as file:
            return file.read()

    @classmethod
    def txt_write(cls, txt_path: Union[str, Path], value: str):
        """写入txt文件"""
        with open(str(txt_path), "w", encoding=cls._encoding_type) as file:
            file.write(value)
