import typing
from pathlib import Path

from .win32_utils.win32_control import Win32Control
from .win32_utils.win32_path import Win32Path
from .win32_utils.win32_visual import Win32Visual


class Win32Util:

    @staticmethod
    def click_left_mouse(click_time: int = 1):
        """点击鼠标左键"""
        Win32Control.click_left_mouse(click_time)

    @staticmethod
    def click_right_mouse(click_time: int = 1):
        """点击鼠标右键"""
        Win32Control.click_right_mouse(click_time)

    @staticmethod
    def close_handle(class_name: str, title: str):
        """关闭窗口"""
        Win32Visual.close_handle(class_name, title)

    @staticmethod
    def find_handle(class_name: str = None, title: str = None, wait_seconds: int = 120) -> int:
        """查找窗口句柄"""
        return Win32Visual.find_handle(class_name, title, wait_seconds)

    @staticmethod
    def find_handles(class_name: str = None, title: str = None, wait_seconds: int = 120) -> typing.List[int]:
        """查找窗口句柄列表"""
        return Win32Visual.find_handles(class_name, title, wait_seconds)

    @staticmethod
    def get_clip_board() -> str:
        """获取剪切板内容"""
        return Win32Control.get_clip_board()

    @staticmethod
    def input(value: str, position: typing.Tuple[int, int] = None, check_input: bool = True, times: int = 1):
        """模拟输入"""
        Win32Control.input(value, position, check_input, times)

    @staticmethod
    def move_mouse(x: int, y: int):
        """移动鼠标到指定坐标"""
        Win32Control.move_mouse(x, y)

    @staticmethod
    def open_file(file_path: typing.Union[Path, str]):
        """打开文件"""
        Win32Path.open_file(str(file_path))

    @staticmethod
    def press_key(*keys: typing.Union[int, str]):
        """模拟按键"""
        Win32Control.press_key(*keys)

    @staticmethod
    def set_clip_board(value: str):
        """设置剪切板"""
        Win32Control.set_clip_board(value)

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
