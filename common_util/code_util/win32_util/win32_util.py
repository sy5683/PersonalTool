import typing
from pathlib import Path

from .win32_utils.win32_control import Win32Control
from .win32_utils.win32_path import Win32Path
from .win32_utils.win32_visual import Win32Visual


class Win32Util:

    @staticmethod
    def find_handle(class_name: str = None, title: str = None, wait_seconds: int = 120) -> int:
        """查找窗口句柄"""
        return Win32Visual.find_handle(class_name, title, wait_seconds)

    @staticmethod
    def find_handles(class_name: str = None, title: str = None, wait_seconds: int = 120) -> typing.List[int]:
        """查找窗口句柄列表"""
        return Win32Visual.find_handles(class_name, title, wait_seconds)

    @staticmethod
    def key_press(key_code_or_name: typing.Union[int, str]):
        """模拟按键"""
        Win32Control.key_press(key_code_or_name)

    @staticmethod
    def open_file(file_path: typing.Union[Path, str]):
        """打开文件"""
        Win32Path.open_file(str(file_path))

    @staticmethod
    def show_window(handle: int, need_admin_right: bool = False):
        """显示窗口"""
        Win32Visual.show_window(handle, need_admin_right)

    @staticmethod
    def upload(file_path: typing.Union[Path, str], wait_seconds: int):
        """上传文件"""
        Win32Visual.upload(str(file_path), wait_seconds)

    @staticmethod
    def wait_handle_disappear(class_name: str = None, title: str = None, wait_seconds: int = 120) -> bool:
        """等待窗口消失"""
        return Win32Visual.wait_handle_disappear(class_name, title, wait_seconds)
