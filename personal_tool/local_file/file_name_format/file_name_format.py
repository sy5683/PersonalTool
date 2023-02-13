import os.path
import os.path
import re
import tkinter
from tkinter import filedialog

import win32api

from personal_tool.base.tool_base import ToolBase


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
        for file_name in sorted(os.listdir(self.directory_path)):
            file_stem, file_suffix = os.path.splitext(file_name)
            # 1) 更改文件名
            if start_number:
                file_stem = str(start_number).zfill(3)
            # 2) 更改文件后缀
            if suffix:
                file_suffix = suffix if suffix.startswith(".") else f".{suffix}"
            else:
                if re.search(r"\.webp$", file_suffix):
                    file_suffix = ".jpg"
            # 3) 重命名文件
            new_file_name = f"{file_stem}{file_suffix}"
            if file_name != new_file_name:
                self._rename(file_name, new_file_name)

    def _rename(self, file_name_from: str, file_name_to: str):
        """文件重命名"""
        file_path_from = os.path.join(self.directory_path, file_name_from)
        file_path_to = os.path.join(self.directory_path, file_name_to)
        os.rename(file_path_from, file_path_to)

    def _directory_path_verification(self):
        """文件校验"""


if __name__ == '__main__':
    file_name_format = FileNameFormat()
    file_name_format.main(FileNameFormat.manga_format)
