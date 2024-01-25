import contextlib
import typing

import numpy
import win32api
import win32con
import win32gui
import win32ui


class Screenshot:

    @classmethod
    def screenshot(cls) -> typing.List[numpy.ndarray]:
        """截图"""
        images = []
        for monitor in win32api.EnumDisplayMonitors(None, None):
            width = monitor[2][2]
            height = monitor[2][3]
            with cls.__screenshot(width, height) as (save_dc, mfc_dc, save_bitmap):
                save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)
                bitmap_ndarray = save_bitmap.GetBitmapBits(True)
                image = numpy.frombuffer(bitmap_ndarray, dtype='uint8')
                image.shape = (height, width, 4)
                images.append(image)
        return images

    @staticmethod
    @contextlib.contextmanager
    def __screenshot(width: int, height: int) -> typing.ContextManager:
        """截图"""
        handle = win32gui.GetDesktopWindow()
        handle_dc = win32gui.GetWindowDC(handle)
        mfc_dc = win32ui.CreateDCFromHandle(handle_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(save_bitmap)
        try:
            yield save_dc, mfc_dc, save_bitmap
        except Exception as e:
            raise e
        finally:
            win32gui.DeleteObject(save_bitmap.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(handle, handle_dc)
