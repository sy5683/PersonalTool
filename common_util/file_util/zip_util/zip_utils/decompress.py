import logging
import os
import re
import shutil
import typing
import zipfile
from pathlib import Path

import py7zr
import rarfile


class Decompress:
    """解压"""

    @classmethod
    def decompress(cls, file_path: Path, password: str) -> typing.List[Path]:
        """解压文件，可以传入压缩文件或者存放多个压缩文件的文件夹"""
        decompress_file_paths = file_path.glob("*.*") if file_path.is_dir() else [file_path]
        decompress_save_paths = []
        for decompress_file_path in decompress_file_paths:
            decompress_save_path = cls.__to_decompress_save_path(decompress_file_path)
            if decompress_save_path.is_dir():
                shutil.rmtree(decompress_save_path)
            cls._decompress_all(decompress_file_path, password)
            decompress_save_paths.append(decompress_save_path)
        return decompress_save_paths

    @classmethod
    def _decompress_all(cls, file_path: Path, password: str):
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
    def _decompress_7z(cls, zip_path: str, save_path: str, password: str) -> str:
        """解压7z文件"""
        # 1) 根据文件二进制数据头判断文件类型
        zip_path = cls.__format_file_path(zip_path, "rar", b"7z\xbc\xaf")
        # 2) 解压7z文件
        logging.info(f"解压7z文件: {zip_path}")
        with py7zr.SevenZipFile(zip_path, "r", password=password) as zip_file:
            try:
                zip_file.extractall(save_path)
            except FileExistsError:
                save_path += "~"
                zip_file.extractall(save_path)
        return save_path

    @classmethod
    def _decompress_rar(cls, zip_path: str, save_path: str, password: str) -> str:
        """解压rar文件"""
        # 1) 根据文件二进制数据头判断文件类型
        zip_path = cls.__format_file_path(zip_path, "rar", b"Rar!")
        # 2) 解压rar文件
        logging.info(f"解压rar文件: {zip_path}")
        rarfile.UNRAR_TOOL = str(Path(__file__).parent.joinpath("UnRAR.exe"))
        with rarfile.RarFile(zip_path) as rar:
            password = password.encode("utf-8")
            try:
                rar.extractall(path=save_path, pwd=password)
            except FileExistsError:
                save_path += "~"
                rar.extractall(path=save_path, pwd=password)
        return save_path

    @classmethod
    def _decompress_zip(cls, zip_path: str, save_path: str, password: str) -> str:
        """解压zip文件"""
        # 1) 根据文件二进制数据头判断文件类型
        if re.search(r"\.docx$|\.xlsx$", zip_path):  # docx和xlsx的二进制数据头与zip相同，因此如果后缀为这两个则直接不运行
            raise PermissionError
        zip_path = cls.__format_file_path(zip_path, "zip", b"PK\x03\x04")
        # 2) 解压zip文件
        logging.info(f"解压zip文件: {zip_path}")
        with zipfile.ZipFile(zip_path, "r") as zip_file:
            password = password.encode("utf-8")
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
