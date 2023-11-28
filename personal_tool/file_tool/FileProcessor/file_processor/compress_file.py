import typing

from common_util.file_util.zip_util.zip_util import ZipUtil


class CompressFile:

    @staticmethod
    def compress(file_paths: typing.Tuple[str]):
        """压缩"""

    @staticmethod
    def decompress(file_paths: typing.Tuple[str]):
        """解压"""
        for file_path in file_paths:
            ZipUtil.decompress(file_path)
