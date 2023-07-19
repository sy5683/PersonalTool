import logging
import os
import tempfile
import tkinter
from tkinter import filedialog
from typing import List


class FileErrorException(Exception):
    """文件错误"""


class FileFeature:
    _file_paths = None
    _save_dir_path = None

    @classmethod
    def get_file_paths(cls) -> List[str]:
        if cls._file_paths is None:
            tkinter.Tk().withdraw()  # 隐藏tk窗口
            cls._file_paths = list(filedialog.askopenfilenames())
        return cls._file_paths

    @classmethod
    def get_suffix(cls) -> str:
        """获取文件后缀（多文件时必须统一后缀）"""
        file_paths = cls.get_file_paths()
        suffixes = set([os.path.splitext(file_path)[-1] for file_path in file_paths])
        if len(suffixes) != 1:
            logging.warning("选择的文件为不同后缀: %s" % "、".join(suffixes))
            raise FileErrorException
        suffix = list(suffixes)[0]
        return suffix.lower()

    @classmethod
    def get_save_path(cls, file_name: str = '') -> str:
        if cls._save_dir_path is None:
            cls._save_dir_path = tempfile.mkdtemp()
        return os.path.join(cls._save_dir_path, file_name)
