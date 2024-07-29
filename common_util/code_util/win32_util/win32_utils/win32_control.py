import logging
import time

import pyautogui
import pyperclip
import pywintypes
import win32clipboard
import win32con


class Win32Control:
    """鼠标键盘操作选择使用pyautogui而不是win32api，是因为pyautogui可以在Linux中使用"""

    @staticmethod
    def click_left_mouse(click_time: int):
        """点击鼠标左键"""
        pyautogui.click(button='left', clicks=click_time)
        time.sleep(0.1)

    @staticmethod
    def click_right_mouse(click_time: int):
        """点击鼠标右键"""
        pyautogui.click(button='right', clicks=click_time)
        time.sleep(0.1)

    @staticmethod
    def get_clip_board() -> str:
        """获取剪切板内容"""
        win32clipboard.OpenClipboard()
        value = win32clipboard.GetClipboardData(win32con.CF_TEXT)
        win32clipboard.CloseClipboard()
        time.sleep(0.1)
        return value.decode('GBK')

    @staticmethod
    def move_mouse(x: int, y: int):
        """移动鼠标到指定坐标"""
        logging.info(f"移动鼠标至: {x}, {y}")
        pyautogui.moveTo(x, y)
        time.sleep(0.1)

    @staticmethod
    def press_key(*key_names: str):
        """模拟按键"""
        logging.info(f"模拟按键: {'+'.join(key_names)}")
        pyautogui.hotkey(*key_names)
        time.sleep(0.1)

    @staticmethod
    def set_clip_board(value: str):
        """设置剪切板"""
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_TEXT, value.encode('gbk'))
            win32clipboard.CloseClipboard()
            time.sleep(0.1)
        except pywintypes.error:
            pyperclip.copy(value)
