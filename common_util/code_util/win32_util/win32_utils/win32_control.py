import typing

import win32api
import win32con


class Win32Control:

    @classmethod
    def key_press(cls, key_code_or_name: typing.Union[int, str]):
        """模拟按键"""
        if isinstance(key_code_or_name, int):
            key_code = key_code_or_name
        else:
            key_code = ord(key_code_or_name.upper())
            # 允许使用按键名称输入的仅数字与字母
            assert key_code in list(range(48, 58)) + list(range(65, 91)), "暂不支持输入数字与字母之外的字符"
        cls._key_press(key_code)

    @staticmethod
    def _key_press(key_code: int):
        win32api.keybd_event(key_code, 0, 0, 0)
        win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)
