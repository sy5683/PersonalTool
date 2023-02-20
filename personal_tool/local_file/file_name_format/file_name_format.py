import os.path
import os.path
import re
import tkinter
from tkinter import filedialog

import win32api

from base.tool_base import ToolBase


class FileNameFormat(ToolBase):
    """文件名格式化"""

    def __init__(self):
        tkinter.Tk().withdraw()  # 隐藏tk窗口
        self.directory_path = filedialog.askdirectory()

    def main(self, function=None, **kwargs):
        if function:
            function(self, **kwargs)
        # 打开结果文件夹
        win32api.ShellExecute(0, "open", self.directory_path, "", "", 1)

    def manga_format(self, suffix: str = None, start_number: int = None):
        """格式化漫画"""
        manga_names = sorted(os.listdir(self.directory_path), key=lambda x: int(re.sub(r'\D+', '', x)))
        for manga_name in manga_names:
            manga_stem, manga_suffix = os.path.splitext(manga_name)
            # 1) 更改文件名
            if start_number is not None:
                manga_stem = f"temp_{str(start_number).zfill(3)}"
                start_number += 1
            # 2) 更改文件后缀
            if suffix:
                manga_suffix = suffix if suffix.startswith(".") else f".{suffix}"
            else:
                if re.search(r"\.webp$", manga_suffix):
                    manga_suffix = ".jpg"
            # 3) 重命名文件
            new_manga_name = f"{manga_stem}{manga_suffix}"
            if manga_name != new_manga_name:
                self._rename(manga_name, new_manga_name)
        for manga_name in sorted(os.listdir(self.directory_path)):
            self._rename(manga_name, re.sub(r"^temp_", "", manga_name))

    def _rename(self, file_name_from: str, file_name_to: str):
        """文件重命名"""
        file_path_from = os.path.join(self.directory_path, file_name_from)
        file_path_to = os.path.join(self.directory_path, file_name_to)
        os.rename(file_path_from, file_path_to)

    def _directory_path_verification(self):
        """文件校验"""


if __name__ == '__main__':
    file_name_format = FileNameFormat()
    file_name_format.main(FileNameFormat.manga_format, start_number=1)
