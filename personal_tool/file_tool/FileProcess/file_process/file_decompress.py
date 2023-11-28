import typing


class FileDecompress:

    @staticmethod
    def decompress(file_paths: typing.Tuple[str]):
        """解压"""
        for file_path in file_paths:
            print(file_path)
