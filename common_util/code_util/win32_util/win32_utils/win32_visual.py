import logging
import time
import typing

import pywintypes
import win32con
import win32gui
from win32com import client


class Win32Visual:

    @classmethod
    def find_handle(cls, class_name: str, title: str, wait_seconds: int) -> int:
        """查找窗口句柄"""
        for _ in range(wait_seconds):
            handles = cls._find_handles(class_name, title)
            if handles:
                return handles[0]
            if wait_seconds > 1:
                time.sleep(1)
        logging.warning(f"未找到窗口: class_name={class_name}, title={title}")
        return 0

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

    @staticmethod
    def show_window(handle: int, need_admin_right: bool):
        """显示窗口"""
        if not handle:
            return
        if win32gui.GetForegroundWindow() != handle:
            return
        # 有些电脑需要管理员权限才能让窗口最前
        if need_admin_right:
            client.Dispatch("WScript.Shell").SendKeys('%')
        # 全屏显示窗口
        # 无限制窗口最前时，windows可能因为安全问题会报错并无法最前，因此这里捕捉一下
        try:
            win32gui.BringWindowToTop(handle)
        except pywintypes.error:
            pass
        try:
            win32gui.ShowWindow(handle, win32con.SW_SHOWNOACTIVATE)
        except pywintypes.error:
            pass
        try:
            win32gui.SetForegroundWindow(handle)
        except pywintypes.error:
            pass
        time.sleep(1)

    @classmethod
    def upload(cls, file_path: str, wait_seconds: int):
        """上传文件"""
        # 一级窗口
        dialog = cls.find_handle("#32770", "打开", wait_seconds)
        # 二级窗口
        combobox_ex32 = win32gui.FindWindowEx(dialog, 0, 'Comboboxex32', None)
        # 三级窗口
        combobox = win32gui.FindWindowEx(combobox_ex32, 0, 'Combobox', None)
        # 四级窗口-文件路经输入框
        edit = win32gui.FindWindowEx(combobox, 0, 'Edit', None)
        # 二级窗口-打开按钮
        button = win32gui.FindWindowEx(dialog, 0, "Button", "打开(&0)")
        time.sleep(1)  # 切换完窗口之后需要稍微等待一下
        # 操作-发送文件路经
        win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, file_path)
        time.sleep(1)  # 演示等待一秒
        # 点击打开按钮
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)

    @staticmethod
    def _find_handles(class_name: str, title: str) -> typing.List[int]:
        """查找窗口句柄列表"""

        def _filter_handle(handle: int, _handles: list):
            if not win32gui.IsWindowVisible(handle):
                return
            if class_name and class_name != win32gui.GetClassName(handle):
                return
            if title and title != win32gui.GetWindowText(handle):
                return
            _handles.append(handle)

        handles = []
        win32gui.EnumWindows(_filter_handle, handles)
        return handles
