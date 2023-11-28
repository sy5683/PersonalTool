import re
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
        try:
            save_path = str(save_path)
            cls._decompress_file(str(file_path), save_path)
        except FileExistsError:
            save_path += "~"
            cls._decompress_file(str(file_path), save_path)
        # 2) 遍历解压出来的文件，递归其中的压缩包
        for decompress_path in Path(save_path).glob("*"):
            # 2.1) 解压完成后的文件可能因为格式原因出现乱码，因此需要处理一下
            try:
                file_name = decompress_path.name.encode("cp437").decode("GBK")
                decompress_path = decompress_path.rename(decompress_path.parent.joinpath(file_name))
            except UnicodeEncodeError:
                pass
            # 2.2) 递归解压被解压出来的文件
            cls._decompress_all(decompress_path, cls.__to_decompress_save_path(decompress_path))

    @classmethod
    def _decompress_file(cls, file_path: str, save_path: str):
        """解压文件"""
        cls.__decompress_zip(file_path, save_path)
        cls.__decompress_rar(file_path, save_path)

    @staticmethod
    def __decompress_rar(file_path: str, save_path: str):
        """解压rar文件"""
        # 1) 根据文件二进制数据头判断文件类型
        try:
            with open(file_path, "rb") as file:
                if not re.match(b"Rar!", file.read()):
                    return
        except PermissionError:
            return
        # 2) 解压rar文件
        rarfile.UNRAR_TOOL = str(Path(__file__).parent.joinpath("UnRAR.exe"))
        with rarfile.RarFile(file_path) as rar:
            rar.extractall(path=save_path)

    @staticmethod
    def __decompress_zip(file_path: str, save_path: str):
        """解压zip文件"""
        # 1) 根据文件二进制数据头判断文件类型
        try:
            with open(file_path, "rb") as file:
                if not re.match(b"PK\x03\x04\x14\x00\x00\x00\x08\x00", file.read()):
                    return
        except PermissionError:
            return
        # 2) 解压zip文件
        shutil.unpack_archive(file_path, extract_dir=save_path, format='zip')

    @staticmethod
    def __to_decompress_save_path(decompress_path: Path) -> Path:
        return decompress_path.parent.joinpath(decompress_path.stem)
