import ctypes
import ctypes.wintypes
import logging
import time
import typing

import numpy
import pywintypes
import win32api
import win32con
import win32gui
import win32ui
from win32com import client


class Win32Visual:

    @classmethod
    def screenshot(cls, handle: int) -> typing.Generator[numpy.ndarray, None, None]:
        """截图"""
        # 获取所有显示器的系统分辨率
        for monitor in win32api.EnumDisplayMonitors():
            width, height = monitor[2][2], monitor[2][3]
            # 跳过被隐藏的显示器
            if not width or not height:
                continue
            if handle:
                left, top, right, bottom = cls._get_window_rect_ctypes(handle)
            else:
                left, top, right, bottom = 0, 0, width, height
            yield cls._screenshot(left, top, right, bottom)

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
        try:
            win32gui.ShowWindow(handle, win32con.SW_SHOWNA)
            win32gui.SetForegroundWindow(handle)
        except pywintypes.error as e:
            # 无限制窗口最前时，windows可能因为安全问题会报错并无法最前，因此这里捕捉一下
            logging.warning(e)
        time.sleep(1)

    @staticmethod
    def _get_window_rect_ctypes(handle: int) -> typing.Tuple[int, int, int, int]:
        """获取窗口准确坐标（不包括外侧边框）"""
        rect = ctypes.wintypes.RECT()
        ctypes.windll.dwmapi.DwmGetWindowAttribute(
            ctypes.wintypes.HWND(handle),
            ctypes.wintypes.DWORD(9),
            ctypes.byref(rect),
            ctypes.sizeof(rect)
        )
        return int(rect.left), int(rect.top), int(rect.right), int(rect.bottom)

    @staticmethod
    def _screenshot(left: int, top: int, right: int, bottom: int) -> numpy.ndarray:
        """截图"""
        width = right - left
        height = bottom - top
        # 根据窗口句柄获取窗口的设备上下文DC
        handle_dc = win32gui.GetWindowDC(0)
        # 根据窗口的DC获取mfcDC
        mfc_dc = win32ui.CreateDCFromHandle(handle_dc)
        # mfcDC创建可兼容的DC
        save_dc = mfc_dc.CreateCompatibleDC()
        # 创建bitmap准备保存图片
        save_bitmap = win32ui.CreateBitmap()
        # 在内存中创建与指定DC兼容的位图对象
        save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        # 将内存中与指定DC设备兼容的位图对象选入指定DC中
        save_dc.SelectObject(save_bitmap)
        # 截图
        save_dc.BitBlt((0, 0), (width, height), mfc_dc, (left, top), win32con.SRCCOPY)
        # # 可以直接保存bitmap，但是这个方法保存的图片非常大，最好将其转为opencv的ndarray对象进行保存
        # save_bitmap.SaveBitmapFile(save_dc, image_path)
        # 位图转换为opencv的ndarray
        bitmap_ndarray = save_bitmap.GetBitmapBits(True)
        # 位图转换为opencv的ndarray
        opencv_image = numpy.frombuffer(bitmap_ndarray, dtype='uint8')
        opencv_image.shape = (height, width, 4)
        # 删除位图对象以便释放资源
        win32gui.DeleteObject(save_bitmap.GetHandle())
        # 删除内存中的DC对象，释放资源
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(0, handle_dc)
        return opencv_image
