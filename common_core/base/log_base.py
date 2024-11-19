import abc
import logging
import sys
from logging import handlers
from pathlib import Path

from common_util.file_util.file_util.file_util import FileUtil


class LogBase(metaclass=abc.ABCMeta):
    logger = logging.getLogger()
    # 1.1) 设置日志输出格式
    formatter = logging.Formatter("[%(asctime)s]-%(levelname)s-%(filename)s(line:%(lineno)d): %(message)s",
                                  datefmt='%Y-%m-%d %H:%M:%S')
    # 1.2) 设置日志输出等级
    logger.setLevel(logging.INFO)
    # 2) 日志输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    def __init__(self):
        # 3) 日志保存至本地文件
        log_path = self.get_log_path(f"{self._get_subclass_path().parent.stem}.log")
        file_handler = handlers.TimedRotatingFileHandler(log_path, when='D', interval=1, backupCount=90,
                                                         encoding='UTF-8')
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def get_log_path(self, file_name: str = '') -> Path:
        log_path = self._get_subclass_path().parent.joinpath(f"file/logs/{file_name}")
        FileUtil.make_dir(log_path)
        return log_path

    def _get_subclass_path(self):
        return Path(sys.modules[self.__module__].__file__)
