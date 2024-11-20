import logging
import typing
from logging import handlers

from pathlib import Path


class LogInit:
    _logger = None
    _console_handler = None
    _log_paths = []

    @classmethod
    def add_console_handler(cls):
        """日志输出到控制台"""
        if cls._console_handler is not None:
            return
        cls._console_handler = logging.StreamHandler()
        cls._console_handler.setFormatter(cls._get_formatter())
        cls._get_logger().addHandler(cls._console_handler)

    @classmethod
    def add_file_handler(cls, log_path: typing.Union[Path, str]):
        """日志保存至本地文件"""
        if not log_path:
            return
        log_path = Path(log_path)
        if log_path.suffix != ".log":
            logging.warning(f"日志文件路径错误: {log_path}")
            return
        if log_path in cls._log_paths:
            logging.warning(f"日志文件已运行: {log_path}")
            return
        if not log_path.parent.exists():
            log_path.parent.mkdir(exist_ok=True, parents=True)
        cls._file_handler = handlers.TimedRotatingFileHandler(log_path, when='D', interval=1, backupCount=90,
                                                         encoding='UTF-8')
        cls._file_handler.setFormatter(cls._get_formatter())
        cls._get_logger().addHandler(cls._file_handler)
        cls._log_paths.append(log_path)

    @classmethod
    def _get_logger(cls) -> logging.Logger:
        """获取日志对象Logger"""
        if cls._logger is None:
            cls._logger = logging.getLogger()
            # 设置日志输出等级
            cls._logger.setLevel(logging.INFO)
        return cls._logger

    @staticmethod
    def _get_formatter() -> logging.Formatter:
        """获取日志格式"""
        return logging.Formatter("[%(asctime)s]-%(levelname)s-%(filename)s(line:%(lineno)d): %(message)s",
                                 datefmt='%Y-%m-%d %H:%M:%S')  # 设置日志输出格式
