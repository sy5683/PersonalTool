import contextlib
import ctypes
import ctypes.wintypes
import typing

import numpy
import win32con
import win32gui
import win32ui


class Screenshot:

    @classmethod
    def screenshot(cls) -> typing.List[numpy.ndarray]:
        """截图"""
        images = []
        for left, top, width, height in cls.__get_monitors():
            with cls.__screenshot(width, height) as (save_dc, mfc_dc, save_bitmap):
                save_dc.BitBlt((0, 0), (width, height), mfc_dc, (left, top), win32con.SRCCOPY)
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

    @staticmethod
    def __get_monitors() -> typing.Iterable[tuple]:

        monitor_enum_proc = ctypes.WINFUNCTYPE(
            ctypes.c_int,
            ctypes.c_ulong,
            ctypes.c_ulong,
            ctypes.POINTER(ctypes.wintypes.RECT),
            ctypes.c_double,
        )

        class MonitorInfoEXW(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.wintypes.DWORD),
                ("rcMonitor", ctypes.wintypes.RECT),
                ("rcWork", ctypes.wintypes.RECT),
                ("dwFlags", ctypes.wintypes.DWORD),
                ("szDevice", ctypes.wintypes.WCHAR * 32),
            ]

        monitors = []

        def callback(monitor: typing.Any, dc: typing.Any, rect: typing.Any, data: typing.Any) -> int:
            info = MonitorInfoEXW()
            info.cbSize = ctypes.sizeof(MonitorInfoEXW)

            rct = rect.contents
            monitors.append(
                (
                    rct.left,
                    rct.top,
                    rct.right - rct.left,
                    rct.bottom - rct.top,
                )
            )
            return 1

        ctypes.windll.shcore.SetProcessDpiAwareness(2)

        for retry in range(100):
            dc_full = ctypes.windll.user32.GetDC(None)
            if dc_full > 0:
                break
            ctypes.windll.user32.ReleaseDC(dc_full)
        else:
            dc_full = 0
        ctypes.windll.user32.EnumDisplayMonitors(
            dc_full, None, monitor_enum_proc(callback), 0
        )
        ctypes.windll.user32.ReleaseDC(dc_full)

        yield from monitors
