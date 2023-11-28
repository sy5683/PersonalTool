import typing
from pathlib import Path

import numpy

from .win32_utils.win32_path import Win32Path
from .win32_utils.win32_visual import Win32Visual


class Win32Util:

    @staticmethod
    def open_file(file_path: typing.Union[Path, str]):
        """打开文件"""
        Win32Path.open_file(str(file_path))

    @staticmethod
    def screenshot(handle: int = 0) -> typing.Generator[numpy.ndarray, None, None]:
        """截图"""
        return Win32Visual.screenshot(handle)

    @staticmethod
    def show_window(handle: int, need_admin_right: bool = False):
        """显示窗口"""
        Win32Visual.show_window(handle, need_admin_right)
