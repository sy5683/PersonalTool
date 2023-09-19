from pathlib import Path
from typing import Union

import win32api


class Win32Util:

    @staticmethod
    def open_file(file_path: Union[str, Path]):
        """打开文件"""
        win32api.ShellExecute(0, "open", str(file_path), "", "", 1)
