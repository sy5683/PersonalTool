import os
import re
import time
import tkinter
import typing
from pathlib import Path
from tkinter import filedialog

import magic


class ProcessFile:
    """处理文件"""

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

    @staticmethod
    def get_directory_path() -> str:
        """获取文件夹路径"""
        tkinter.Tk().withdraw()  # 隐藏tk窗口
        return filedialog.askdirectory()

    @staticmethod
    def get_file_path() -> str:
        """获取文件路径"""
        tkinter.Tk().withdraw()  # 隐藏tk窗口
        return filedialog.askopenfilename()

    @staticmethod
    def get_file_paths() -> typing.Tuple[str, ...]:
        """获取文件路径列表"""
        tkinter.Tk().withdraw()  # 隐藏tk窗口
        return filedialog.askopenfilenames()

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

    @staticmethod
    def get_root_paths() -> typing.List[str]:
        """获取电脑根路径列表"""
        return [root_dir for root_dir in [f"{chr(65 + index)}:\\" for index in range(26)] if os.path.exists(root_dir)]

    @staticmethod
    def make_dir(file_path: Path):
        """新建文件夹"""
        # pathlib.mkdir指向的必须为文件夹，因此如果路径为文件时则新建其父级文件夹
        dir_path = file_path.parent if file_path.suffix else file_path
        dir_path.mkdir(exist_ok=True, parents=True)  # parents参数保证递归创建文件目录

    @staticmethod
    def wait_file_appear(file_path: Path, wait_seconds: int) -> bool:
        """等待文件出现"""
        for _ in range(wait_seconds):
            try:
                if file_path.suffix:  # 根据是否有后缀名判断等待的是不是文件
                    if file_path.is_file():
                        return True
                else:  # 当等待的文件为文件夹时，还需要判断其中是否有文件出现
                    try:
                        next(file_path.glob("*.*"))
                    except StopIteration:
                        continue
                    return True
            finally:
                if wait_seconds > 1:
                    time.sleep(1)
        return False
