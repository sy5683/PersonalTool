import pathlib
import typing

from .zip_utils.compress import Compress
from .zip_utils.decompress import Decompress


class ZipUtil:

    @staticmethod
    def compress(file_path: typing.Union[pathlib.Path, str], compress_name: str = ''):
        """压缩文件"""
        return Compress.compress(pathlib.Path(file_path), compress_name)

    @staticmethod
    def decompress(file_path: typing.Union[pathlib.Path, str],
                   password: str = None) -> typing.Generator[pathlib.Path, None, None]:
        """解压文件"""
        return Decompress.decompress(pathlib.Path(file_path), password)
