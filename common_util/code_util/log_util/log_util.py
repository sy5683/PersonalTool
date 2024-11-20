import typing
from pathlib import Path

from .log_utils.log_init import LogInit


class LogUtil:

    @classmethod
    def add_console_handler(cls):
        """日志输出到控制台"""
        LogInit.add_console_handler()

    @classmethod
    def add_file_handler(cls, log_path: typing.Union[Path, str] = None):
        """日志保存至本地文件"""
        LogInit.add_file_handler(log_path)
