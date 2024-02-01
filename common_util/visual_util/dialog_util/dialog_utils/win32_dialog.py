import threading
import time

import win32api
import win32con
import win32gui


class Win32Dialog:

    @staticmethod
    def message_box(message: str, title: str, disable_close: bool):
        """消息通知"""

        def set_top_dialog():
            """设置窗口style"""
            for _ in range(10):
                window = win32gui.FindWindow(None, title)
                if window:
                    if disable_close:
                        win32gui.EnableMenuItem(win32gui.GetSystemMenu(window, False), win32con.SC_CLOSE,
                                                win32con.MF_BYCOMMAND | win32con.MF_DISABLED | win32con.MF_GRAYED)
                    win32gui.SetWindowPos(window, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
                    return
                time.sleep(1)

        threading.Thread(target=set_top_dialog, args=(), daemon=True).start()
        win32api.MessageBox(0, message, title, win32con.MB_OK)
