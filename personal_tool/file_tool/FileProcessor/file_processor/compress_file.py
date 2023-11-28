import typing

from common_util.file_util.file_util.file_util import FileUtil


class CompressFile:

    @staticmethod
    def compress(file_paths: typing.Tuple[str]):
        """压缩"""

    @staticmethod
    def decompress(file_paths: typing.Tuple[str]):
        """解压"""
        for file_path in file_paths:
            original_type = FileUtil.get_original_type(file_path)
            print(original_type)
