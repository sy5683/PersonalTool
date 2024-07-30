import logging
import time
import typing

import pyautogui
import pyperclip


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
        return pyperclip.paste()

    @classmethod
    def input(cls, value: str, position: typing.Tuple[int, int], check_input: bool, times: int):
        """模拟输入"""
        if position is not None:
            cls.move_mouse(position[0], position[1])
            cls.click_left_mouse(times)
        # 全选粘贴替换文本
        cls.press_key("ctrl", "a")
        cls.set_clip_board(value)
        cls.press_key("ctrl", "v")
        # 判断有没有粘贴成功
        if check_input:
            cls.set_clip_board()
            cls.press_key("ctrl", "a")
            cls.press_key("ctrl", "c")
            if cls.get_clip_board() != value:
                raise RuntimeError("输入失败")

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
    def set_clip_board(value: str = ''):
        """设置剪切板"""
        pyperclip.copy(value)
