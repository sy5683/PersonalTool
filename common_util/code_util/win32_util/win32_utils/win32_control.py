import time

import win32api
import win32con


class Win32Control:

    @classmethod
    def key_press(cls, key_name: str):
        """模拟按键"""
        key_code = ord(key_name.upper())
        assert key_code in list(range(48, 58)) + list(range(65, 91)), "暂不支持字母与数字之外的字符"
        win32api.keybd_event(key_code, 0, 0, 0)
        win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.5)
