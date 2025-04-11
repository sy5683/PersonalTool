import abc
import logging
import os
import re
import shutil
import time
import typing
from pathlib import Path

import magic


class ProcessFile:

    @staticmethod
    def delete_file(file_path: Path):
        """删除文件"""
        try:
            if file_path.is_dir():
                shutil.rmtree(file_path)
            else:
                os.chmod(file_path, 0o777)  # 修改只读文件权限
                os.remove(file_path)
        except PermissionError:
            pass

    @classmethod
    def format_path(cls, file_path: Path) -> Path:
        """
        格式化路径
        如果文件所在文件夹路径不存在，则新建其祖辈文件夹
        如果文件已存在，则自增编号（模拟windows操作）
        """
        add_num = 0
        file_name = file_path.stem
        while file_path.exists():
            add_num += 1
            file_path = file_path.parent.joinpath(f"{file_name}({add_num}){file_path.suffix}")
        cls.make_dir(file_path)
        return file_path

    @classmethod
    @abc.abstractmethod
    def get_directory_path(cls) -> str:
        """获取文件夹路径"""
        return cls.__get_subclass().get_directory_path()

    @classmethod
    @abc.abstractmethod
    def get_file_path(cls) -> str:
        """获取文件路径"""
        return cls.__get_subclass().get_file_path()

    @classmethod
    @abc.abstractmethod
    def get_file_paths(cls) -> typing.Literal[""] | typing.Tuple[str, ...]:
        """获取文件路径列表"""
        return cls.__get_subclass().get_file_paths()

    @staticmethod
    def get_file_size(file_path: Path) -> float:
        """获取文件大小"""
        if file_path.is_dir():
            file_size = sum(each.stat().st_size for each in Path(file_path).glob("**/*") if each.is_file())
        else:
            file_size = file_path.stat().st_size
        return file_size  # 返回值为KB，需要其他单位可以在这里除以1024进行处理

    @staticmethod
    def get_original_type(file_path: str) -> str:
        """获取文件原始类型"""
        # 根据文件读取出来的二进制数据开头判断文件类型
        with open(file_path, "rb") as file:
            file_type = magic.Magic().from_buffer(file.read(1024))
        # 根据magic的返回规范文件类型
        if re.search("7-zip archive data", file_type):
            return "7z"
        elif re.search("Composite Document File V2 Document", file_type):
            if re.search(r"\.xls$", file_path):
                return "xls"
            return "doc"
        elif re.search("GIF image data", file_type):
            return "gif"
        elif re.search("JPEG image data", file_type):
            return "jpg"
        elif re.search("PDF document", file_type):
            return "pdf"
        elif re.search("PNG image data", file_type):
            return "png"
        elif re.search("RAR archive data", file_type):
            return "rar"
        elif re.search("text", file_type):
            return "txt"
        elif re.search("Zip archive data", file_type):
            if re.search(r"\.docx$", file_path):
                return "docx"
            elif re.search(r"\.xlsx$", file_path):
                return "xlsx"
            return "zip"
        else:
            print(file_type)
            return "unknown"

    @classmethod
    @abc.abstractmethod
    def get_root_paths(cls) -> typing.List[str]:
        """获取电脑根路径列表"""
        return cls.__get_subclass().get_root_paths()

    @staticmethod
    def make_dir(file_path: Path):
        """新建文件夹"""
        # pathlib.mkdir指向的必须为文件夹，因此如果路径为文件时则新建其父级文件夹
        dir_path = file_path.parent if file_path.suffix else file_path
        dir_path.mkdir(exist_ok=True, parents=True)  # parents参数保证递归创建文件目录

    @classmethod
    @abc.abstractmethod
    def open_file(cls, file_path: str):
        """打开文件"""
        logging.info(f"打开文件: {file_path}")
        if os.path.isfile(file_path):
            cls.__get_subclass().open_file(file_path)
        cls.__get_subclass().open_file(file_path)

    @staticmethod
    def wait_file_appear(file_path: Path, wait_seconds: int):
        """等待文件出现"""
        logging.info(f"等待文件出现: {file_path}")
        for index in range(wait_seconds):
            try:
                # 根据是否有后缀名判断等待的是不是文件，当等待的文件为文件时，判断文件是否存在
                if file_path.suffix:
                    if file_path.is_file():
                        logging.info(f"文件已出现: {file_path}")
                        return True
                # 当等待的文件为文件夹时，还需要判断其中是否有文件出现
                else:
                    try:
                        appear_file_path = next(file_path.glob("*.*"))
                    except StopIteration:
                        continue
                    logging.info(f"文件夹中出现文件: {appear_file_path}")
                    return True
            finally:
                if index != wait_seconds - 1:
                    time.sleep(1)
        # 文件未出现，返回报错
        if file_path.suffix:
            logging.warning(f"未找到文件: {file_path}")
            raise FileExistsError(f"未找到文件: {file_path.name}")
        else:
            logging.warning(f"文件夹中未生成文件: {file_path}")
            raise FileExistsError("文件夹中未生成文件")

    @staticmethod
    def __get_subclass():
        if os.name == "nt":
            from .process_file_windows import ProcessFileWindows
            return ProcessFileWindows
        elif os.name == "posix":
            from .process_file_linux import ProcessFileLinux
            return ProcessFileLinux
        raise Exception(f"未知的操作系统类型: {os.name}")
