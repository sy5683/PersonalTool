import logging
import time
import typing

import pyperclip
import win32api
import win32clipboard
import win32con


class Win32Control:

    @staticmethod
    def get_clip_board() -> str:
        """获取剪切板内容"""
        win32clipboard.OpenClipboard()
        value = win32clipboard.GetClipboardData(win32con.CF_TEXT)
        win32clipboard.CloseClipboard()
        time.sleep(0.1)
        return value.decode('GBK')

    @classmethod
    def press_key(cls, *keys: typing.Union[int, str]):
        """模拟按键"""
        key_codes = [cls.__format_key_code(key) for key in keys]
        for key_code in key_codes:
            logging.info(f"模拟按键: {keys}")
            win32api.keybd_event(key_code, 0, 0, 0)
        time.sleep(0.2)
        for key_code in key_codes:
            win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def set_clip_board(value: str):
        """设置剪切板"""
        # noinspection PyBroadException
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32con.CF_TEXT, value.encode('gbk'))
            win32clipboard.CloseClipboard()
            time.sleep(0.1)
        except Exception:
            pyperclip.copy(value)

    @staticmethod
    def __format_key_code(key: typing.Union[int, str]) -> int:
        if isinstance(key, int):
            key_code = key
        else:
            key_code = int(ord(key.upper()))
            # 允许使用按键名称输入的仅数字与字母
            assert key_code in list(range(48, 58)) + list(range(65, 91)), "暂不支持输入数字与字母之外的字符"
        return key_code
