import shutil
from pathlib import Path

import rarfile


class Decompress:
    """解压"""

    @classmethod
    def decompress(cls, file_path: Path):
        """解压文件，可以传入压缩文件或者存放多个压缩文件的文件夹"""
        decompress_file_paths = file_path.glob("*.*") if file_path.is_dir() else [file_path]
        for decompress_file_path in decompress_file_paths:
            decompress_save_path = cls.__to_decompress_save_path(decompress_file_path)
            if decompress_save_path.is_dir():
                shutil.rmtree(decompress_save_path)
            cls._decompress_all(decompress_file_path, decompress_save_path)

    @classmethod
    def _decompress_all(cls, file_path: Path, save_path: Path):
        """递归解压缩压缩文件中的所有文件"""
        # 1) 解压压缩包
        if file_path.suffix == ".zip":
            cls._decompress_zip(str(file_path), str(save_path))
        elif file_path.suffix == ".rar":
            cls._decompress_rar(str(file_path), str(save_path))
        # 2) 遍历解压出来的文件，递归其中的压缩包
        for decompress_path in save_path.glob("*"):
            # 2.1) 解压完成后的文件可能因为格式原因出现乱码，因此需要处理一下
            decompress_path = cls._format_decompress_name(decompress_path)
            # 2.2) 递归解压被解压出来的文件
            cls._decompress_all(decompress_path, cls.__to_decompress_save_path(decompress_path))

    @staticmethod
    def _decompress_rar(file_path: str, save_path: str):
        """解压rar文件"""
        rarfile.UNRAR_TOOL = str(Path(__file__).parent.joinpath("UnRAR.exe"))
        with rarfile.RarFile(file_path) as rar:
            rar.extractall(path=save_path)

    @staticmethod
    def _decompress_zip(file_path: str, save_path: str):
        """解压zip文件"""
        shutil.unpack_archive(file_path, extract_dir=save_path, format='zip')

    @staticmethod
    def _format_decompress_name(decompress_path: Path) -> Path:
        """解压缩之后的文件，可能因为格式原因出现乱码，因此需要将其处理一下"""
        try:
            file_name = decompress_path.name.encode("cp437").decode("GBK")
            return decompress_path.rename(decompress_path.parent.joinpath(file_name))
        except UnicodeEncodeError:
            return decompress_path

    @staticmethod
    def __to_decompress_save_path(decompress_path: Path) -> Path:
        return decompress_path.parent.joinpath(decompress_path.stem)
