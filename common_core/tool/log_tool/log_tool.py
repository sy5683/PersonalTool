import logging
import typing
from pathlib import Path

from .log_tools.log_init import LogInit


class LogTool:

    @staticmethod
    def add_console_handler(**kwargs):
        """日志输出到控制台"""
        LogInit.add_console_handler(**kwargs)

    @staticmethod
    def add_file_handler(log_path: typing.Union[Path, str], **kwargs):
        """日志保存至本地文件"""
        LogInit.add_file_handler(Path(log_path),**kwargs)

    @staticmethod
    def get_logger(**kwargs) -> logging.Logger:
        """获取日志对象Logger"""
        return LogInit.get_logger(**kwargs)
