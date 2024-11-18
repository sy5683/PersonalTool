import os
import tkinter
import typing
from tkinter import filedialog

from .process_file import ProcessFile


class ProcessFileWindows(ProcessFile):

    @classmethod
    def get_directory_path(cls) -> str:
        """获取文件夹路径"""
        tkinter.Tk().withdraw()  # 隐藏tk窗口
        return filedialog.askdirectory()

    @classmethod
    def get_file_path(cls) -> str:
        """获取文件路径"""
        tkinter.Tk().withdraw()  # 隐藏tk窗口
        return filedialog.askopenfilename()

    @classmethod
    def get_file_paths(cls) -> typing.Literal[""] | typing.Tuple[str, ...]:
        """获取文件路径列表"""
        tkinter.Tk().withdraw()  # 隐藏tk窗口
        return filedialog.askopenfilenames()

    @classmethod
    def get_root_paths(cls) -> typing.List[str]:
        """获取电脑根路径列表"""
        return [root_dir for root_dir in [f"{chr(65 + index)}:\\" for index in range(26)] if os.path.exists(root_dir)]
