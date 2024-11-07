import ctypes
import typing

import numpy
import screeninfo
import win32con
import win32gui
import win32ui

from .screenshot import Screenshot


class ScreenshotWindows(Screenshot):

    @classmethod
    def get_screenshot_images(cls) -> typing.List[numpy.ndarray]:
        """获取截图图片"""
        try:
            return cls._get_win32_screenshot_images()
        except ctypes.ArgumentError:
            # 可能会有 argument 1: <class 'OverflowError'>: int too long to convert 问题，因此捕捉后特殊处理
            return cls._get_pil_screenshot_images()

    @staticmethod
    def _get_win32_screenshot_images() -> typing.List[numpy.ndarray]:
        """获取win32的截图图片"""
        images = []
        for monitor in screeninfo.get_monitors():
            handle = win32gui.GetDesktopWindow()
            handle_dc = win32gui.GetWindowDC(handle)
            mfc_dc = win32ui.CreateDCFromHandle(handle_dc)
            save_dc = mfc_dc.CreateCompatibleDC()
            save_bitmap = win32ui.CreateBitmap()
            save_bitmap.CreateCompatibleBitmap(mfc_dc, monitor.width, monitor.height)
            save_dc.SelectObject(save_bitmap)
            try:
                save_dc.BitBlt((0, 0), (monitor.width, monitor.height), mfc_dc, (monitor.x, monitor.y),
                               win32con.SRCCOPY)
                bitmap_ndarray = save_bitmap.GetBitmapBits(True)
                image = numpy.frombuffer(bitmap_ndarray, dtype='uint8')
                image.shape = (monitor.height, monitor.width, 4)
                images.append(image)
            finally:
                win32gui.DeleteObject(save_bitmap.GetHandle())
                save_dc.DeleteDC()
                mfc_dc.DeleteDC()
                win32gui.ReleaseDC(handle, handle_dc)
        return images
