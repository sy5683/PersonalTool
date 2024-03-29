import logging
import os

import pywintypes
import win32api


class Win32Path:

    @classmethod
    def open_file(cls, file_path: str):
        """打开文件"""
        logging.info(f"打开文件: {file_path}")
        if os.path.isfile(file_path):
            cls._open_file(os.path.dirname(file_path))
        cls._open_file(file_path)

    @staticmethod
    def _open_file(file_path: str):
        """打开文件"""
        try:
            win32api.ShellExecute(0, "open", file_path, "", "", 1)
        except pywintypes.error:
            raise FileExistsError(f"文件不存在: {file_path}")
