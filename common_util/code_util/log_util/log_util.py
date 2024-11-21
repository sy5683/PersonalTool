import logging
import typing
from pathlib import Path

from .log_utils.log_init import LogInit


class LogUtil:

    @staticmethod
    def add_console_handler():
        """日志输出到控制台"""
        LogInit.add_console_handler()

    @staticmethod
    def add_file_handler(log_path: typing.Union[Path, str] = ''):
        """日志保存至本地文件"""
        LogInit.add_file_handler(Path(log_path))

    @staticmethod
    def get_logger(log_name: str = '') -> logging.Logger:
        """获取日志对象Logger"""
        return LogInit.get_logger(log_name)
