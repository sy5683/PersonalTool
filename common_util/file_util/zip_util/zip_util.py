import typing
from pathlib import Path

from .zip_utils.decompress import Decompress


class ZipUtil:

    @classmethod
    def decompress(cls, file_path: typing.Union[Path, str], password: str = None) -> typing.Generator[Path, None, None]:
        """解压文件"""
        return Decompress.decompress(Path(file_path), password)
