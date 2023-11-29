import logging
import os.path
import re
import shutil
import zipfile
from pathlib import Path

import rarfile


class Decompress:
    """解压"""

    @classmethod
    def decompress(cls, file_path: Path, password: bytes):
        """解压文件，可以传入压缩文件或者存放多个压缩文件的文件夹"""
        decompress_file_paths = file_path.glob("*.*") if file_path.is_dir() else [file_path]
        for decompress_file_path in decompress_file_paths:
            decompress_save_path = cls.__to_decompress_save_path(decompress_file_path)
            if decompress_save_path.is_dir():
                shutil.rmtree(decompress_save_path)
            cls._decompress_all(decompress_file_path, password)

    @classmethod
    def _decompress_all(cls, file_path: Path, password: bytes):
        """递归解压缩压缩文件中的所有文件"""
        decompress_file_paths = file_path.glob("*.*") if file_path.is_dir() else [file_path]
        for decompress_file_path in decompress_file_paths:
            decompress_save_path = cls.__to_decompress_save_path(decompress_file_path)
            save_path = str(decompress_save_path)
            if decompress_save_path.is_dir():
                save_path += "~"
            # 1.1) 解压压缩包
            decompress_save_path = cls._decompress_file(file_path=str(decompress_file_path), save_path=save_path,
                                                        password=password)
            if not decompress_save_path:
                return
            # 1.2) 解压完成后的文件可能因为格式原因出现乱码，格式化一下
            cls.__format_decompress_file(decompress_save_path)
            # 2) 遍历解压出来的文件，递归解压被解压出来的文件
            for decompress_path in Path(decompress_save_path).glob("*"):
                cls._decompress_all(decompress_path, password)

    @classmethod
    def _decompress_file(cls, **kwargs) -> str:
        """解压文件"""
        for decompress_function in [cls._decompress_zip, cls._decompress_rar]:
            try:
                return decompress_function(**kwargs)
            except PermissionError:
                pass

    @classmethod
    def _decompress_rar(cls, file_path: str, save_path: str, password: bytes) -> str:
        """解压rar文件"""
        # 1) 根据文件二进制数据头判断文件类型
        file_path = cls.__format_file_path(file_path, "rar", b"Rar!")
        # 2) 解压rar文件
        logging.info(f"解压rar文件: {file_path}")
        rarfile.UNRAR_TOOL = str(Path(__file__).parent.joinpath("UnRAR.exe"))
        with rarfile.RarFile(file_path) as rar:
            try:
                rar.extractall(path=save_path, pwd=password)
            except FileExistsError:
                save_path += "~"
                rar.extractall(path=save_path, pwd=password)
        return save_path

    @classmethod
    def _decompress_zip(cls, file_path: str, save_path: str, password: bytes) -> str:
        """解压zip文件"""
        # 1) 根据文件二进制数据头判断文件类型
        file_path = cls.__format_file_path(file_path, "zip", b"PK")
        # 2) 解压zip文件
        logging.info(f"解压zip文件: {file_path}")
        with zipfile.ZipFile(file_path, "r") as zip_file:
            try:
                zip_file.extractall(save_path, pwd=password)
            except FileExistsError:
                save_path += "~"
                zip_file.extractall(save_path, pwd=password)
        return save_path

    @staticmethod
    def __format_decompress_file(save_path: str):
        """解压完成后的文件可能因为格式原因出现乱码，格式化一下"""
        for file_path in Path(save_path).rglob("*"):
            try:
                file_name = file_path.name.encode("cp437").decode("GBK")
                file_path.rename(file_path.parent.joinpath(file_name))
            except UnicodeEncodeError:
                pass

    @staticmethod
    def __format_file_path(file_path: str, suffix: str, start_bytes: bytes):
        try:  # 为了方便捕获，这里抛出与可能出现问题相同的异常
            with open(file_path, "rb") as file:
                if not re.match(start_bytes, file.read()):
                    raise PermissionError
        except FileNotFoundError:
            raise PermissionError
        if suffix not in os.path.splitext(file_path)[-1].lower():
            new_file_path = f"{file_path}.{suffix}"
            os.rename(file_path, new_file_path)
            file_path = new_file_path
        return file_path

    @staticmethod
    def __to_decompress_save_path(decompress_path: Path) -> Path:
        return decompress_path.parent.joinpath(decompress_path.stem)
