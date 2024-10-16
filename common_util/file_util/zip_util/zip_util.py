import typing
from pathlib import Path

from .zip_utils.compress import Compress
from .zip_utils.decompress import Decompress


class ZipUtil:

    @staticmethod
    def compress(file_path: typing.Union[Path, str], compress_name: str = ''):
        """压缩文件"""
        return Compress.compress(Path(file_path), compress_name)

    @staticmethod
    def decompress(file_path: typing.Union[Path, str], password: str = None) -> typing.Generator[Path, None, None]:
        """解压文件"""
        return Decompress.decompress(Path(file_path), password)
