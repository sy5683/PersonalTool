import os
import re
import time
import tkinter
import typing
from enum import Enum
from pathlib import Path
from tkinter import filedialog


class _FileOriginalType(Enum):
    _7z = {'binary_head': b"7z"}
    exe = {'binary_head': b"MZ|MZx"}
    gif = {'binary_head': b"GIF89a"}
    jpg = {'binary_head': b"\xff\xd8\xff"}
    mp3 = {'binary_head': b"ID3"}
    pdf = {'binary_head': b"%PDF"}
    png = {'binary_head': b"\x89PNG"}
    rar = {'binary_head': b"Rar!"}
    zip = {'binary_head': b"PK"}

    def to_binary_head(self) -> bytes:
        return self.value['binary_head']


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
    def get_file_path() -> str:
        """获取文件路径"""
        tkinter.Tk().withdraw()  # 隐藏tk窗口
        return filedialog.askopenfilename()

    @staticmethod
    def get_file_paths() -> typing.Tuple[str]:
        """获取文件路径列表"""
        tkinter.Tk().withdraw()  # 隐藏tk窗口
        return filedialog.askopenfilenames()

    @staticmethod
    def get_original_type(file_path: str) -> str:
        """获取文件原始类型"""
        assert os.path.exists(file_path), f"文件路径不存在: {file_path}"
        # 根据文件读取出来的二进制数据开头判断文件类型
        try:
            with open(file_path, "rb") as file:
                content = file.read()
                for file_original_type in _FileOriginalType:
                    if re.match(file_original_type.to_binary_head(), content):
                        return file_original_type.name
                else:
                    print(content)
                    return "unknown"
        except PermissionError:
            return "folder"

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
                time.sleep(1)
        return False
