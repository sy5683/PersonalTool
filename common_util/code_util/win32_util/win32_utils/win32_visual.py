import logging
import time
import traceback
import typing

import pywintypes
import win32con
import win32gui
import win32process
from win32api import CloseHandle, OpenProcess, TerminateProcess
from win32com import client


class Win32Visual:

    @classmethod
    def close_handle(cls, class_name: str, title: str):
        """关闭窗口"""
        try:
            handler = cls.find_handle(class_name, title, 1)
            assert handler
        except AssertionError:
            return
        thread_id, process_id = win32process.GetWindowThreadProcessId(handler)
        if thread_id:
            # noinspection PyBroadException
            try:
                process = OpenProcess(1, False, process_id)
                TerminateProcess(process, 0)
                CloseHandle(process)
            except Exception:
                logging.error(traceback.format_exc())
            time.sleep(1)

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
        except Exception:
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
