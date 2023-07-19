import os
import re
import tkinter
from pathlib import Path
from tkinter import filedialog


class FileFeature:
    _directory_path = None

    @classmethod
    def get_directory_path(cls) -> Path:
        if cls._directory_path is None:
            tkinter.Tk().withdraw()  # 隐藏tk窗口
            cls._directory_path = Path(filedialog.askdirectory())
        return cls._directory_path

    @staticmethod
    def sorted_glob(path: Path, sorted_format_function=None):
        def get_stem(stem):
            return stem if sorted_format_function is None else sorted_format_function(stem)

        return sorted(path.glob("*.*"), key=lambda x: int(re.sub(r"\D+", "", str(get_stem(x.stem))) + "0"))

    @staticmethod
    def file_rename(path: Path, new_path: Path = None):
        """重命名"""
        if new_path is None:
            # 重新生成文件路径，防止其父辈文件夹中名称有temp开头的文件夹被误重命名
            new_path = path.parent.joinpath(re.sub(r"^temp_", "", path.stem) + path.suffix)
        if path != new_path:
            os.rename(path, new_path)
