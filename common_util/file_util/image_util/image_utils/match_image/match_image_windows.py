import ctypes
import typing
from ctypes import wintypes

from .match_image import MatchImage


class MatchImageWindows(MatchImage):

    @classmethod
    def get_window_rect(cls, handle: int) -> typing.Tuple[int, int, int, int]:
        """获取窗口坐标"""
        rect = wintypes.RECT()
        ctypes.windll.dwmapi.DwmGetWindowAttribute(ctypes.wintypes.HWND(handle), ctypes.wintypes.DWORD(9),
                                                   ctypes.byref(rect), ctypes.sizeof(rect))
        return rect.left, rect.top, rect.right, rect.bottom
