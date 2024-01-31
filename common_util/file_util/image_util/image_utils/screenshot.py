import os
import tempfile
import typing
from pathlib import Path

import numpy
import screeninfo
import win32con
import win32gui
import win32ui

from .process_opencv_image import ProcessOpenCVImage


class Screenshot:

    @classmethod
    def screenshot(cls, save_path: typing.Union[Path, str]) -> typing.List[str]:
        """截图"""
        save_paths = []
        save_path, suffix = os.path.splitext(f"{tempfile.mktemp()}.jpg" if save_path is None else str(save_path))
        for index, image in enumerate(cls.get_screenshot_image()):
            _save_path = (save_path + f"_{index}" if index else save_path) + suffix
            ProcessOpenCVImage.save_image(image, _save_path)
            save_paths.append(_save_path)
        return save_paths

    @staticmethod
    def get_screenshot_image() -> typing.List[numpy.ndarray]:
        """获取截图图片"""
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
