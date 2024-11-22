import logging
import time
import typing
from logging import handlers
from pathlib import Path

from .log_config import LogConfig


class LogInit:

    @classmethod
    def add_console_handler(cls, **kwargs):
        """日志输出到控制台"""
        handler = cls._get_handler(logging.StreamHandler, **kwargs)
        if handler:
            logging.warning("控制台日志只运行一行")
            return
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(LogConfig.formatter)
        cls.get_logger(**kwargs).addHandler(console_handler)

    @classmethod
    def add_file_handler(cls, log_path: Path, **kwargs):
        """日志保存至本地文件"""
        if not log_path:
            return
        if log_path.suffix != ".log":
            logging.warning(f"日志文件路径错误: {log_path}")
            return
        handler: logging.FileHandler = cls._get_handler(logging.FileHandler, **kwargs)
        if handler:
            logging.warning(f"日志文件已运行: {handler.baseFilename}")
            return
        if not log_path.parent.exists():
            log_path.parent.mkdir(exist_ok=True, parents=True)
        # 对已有日志文件进行切割处理
        if log_path.exists():
            file_create_time = time.strftime("%Y-%m-%d", time.localtime(log_path.stat().st_ctime))
            if file_create_time != time.strftime("%Y-%m-%d"):
                log_path.rename(f"{log_path}.{file_create_time}")
        file_handler = handlers.TimedRotatingFileHandler(log_path, when='D', interval=1, backupCount=90,
                                                         encoding='UTF-8')
        file_handler.setFormatter(LogConfig.formatter)
        cls.get_logger(**kwargs).addHandler(file_handler)

    @staticmethod
    def get_logger(**kwargs) -> logging.Logger:
        """获取日志对象Logger"""
        # getLogger方法自带缓存，不需要再额外实现缓存
        logger = kwargs.get("logger")
        if logger:
            return logger
        logger = logging.getLogger(kwargs.get("log_name"))
        logger.setLevel(logging.INFO)  # 设置日志输出等级
        return logger

    @classmethod
    def _get_handler(cls, handler_type: typing.Type[logging.Handler], **kwargs) -> typing.Union[logging.Handler, None]:
        """获取日志handler"""
        logger = cls.get_logger(**kwargs)
        for handler in logger.handlers:
            if isinstance(handler, handler_type):
                return handler
