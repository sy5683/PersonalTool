import abc
import logging
import os
import time
import typing


class Win32Visual:

    @classmethod
    @abc.abstractmethod
    def close_handle(cls, class_name: str, title: str):
        """关闭窗口"""
        cls.__get_subclass().close_handle(class_name, title)

    @classmethod
    def find_handle(cls, class_name: str, title: str, wait_seconds: int) -> int:
        """查找窗口句柄"""
        handles = cls.find_handles(class_name, title, wait_seconds)
        return handles[0] if handles else 0

    @classmethod
    def find_handles(cls, class_name: str, title: str, wait_seconds: int) -> typing.List[int]:
        """查找窗口句柄列表"""
        for _ in range(wait_seconds):
            handles = cls._find_handles(class_name, title)
            if handles:
                return handles
            if wait_seconds > 1:
                time.sleep(1)
        logging.warning(f"未找到窗口: class_name={class_name}, title={title}")
        return []

    @classmethod
    @abc.abstractmethod
    def show_window(cls, handle: int, need_admin_right: bool):
        """显示窗口"""
        cls.__get_subclass().show_window(handle, need_admin_right)

    @classmethod
    @abc.abstractmethod
    def upload(cls, file_path: str, wait_seconds: int):
        """上传文件"""
        cls.__get_subclass().upload(file_path, wait_seconds)

    @classmethod
    def wait_handle_disappear(cls, class_name: str, title: str, wait_seconds: int) -> bool:
        """等待窗口消失"""
        for _ in range(wait_seconds):
            handles = cls._find_handles(class_name, title)
            if not handles:
                return True
            if wait_seconds > 1:
                time.sleep(1)
        logging.warning(f"窗口存在超时: class_name={class_name}, title={title}")
        return False

    @classmethod
    @abc.abstractmethod
    def _find_handles(cls, class_name: str, title: str) -> typing.List[int]:
        """查找窗口句柄列表"""
        return cls.__get_subclass()._find_handles(class_name, title)

    @staticmethod
    def __get_subclass():
        if os.name == "nt":
            from .win32_visual_windows import Win32VisualWindows
            return Win32VisualWindows
        elif os.name == "posix":
            from .win32_visual_linux import Win32VisualLinux
            return Win32VisualLinux
        raise Exception(f"未知的操作系统类型: {os.name}")
