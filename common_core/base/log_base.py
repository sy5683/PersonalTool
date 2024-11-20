import abc
import logging
import sys
from logging import handlers
from pathlib import Path


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
        log_path = self.get_subclass_path(f"file/logs/{self.get_subclass_path().parent.stem}.log")
        file_handler = handlers.TimedRotatingFileHandler(log_path, when='D', interval=1, backupCount=90,
                                                         encoding='UTF-8')
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def get_subclass_path(self, file_name: str = None) -> Path:
        """
        获取子类文件路径
        传入file_name时，会生成子类同级的路径
        """
        file_path = Path(sys.modules[self.__module__].__file__)
        if file_name:
            file_path = file_path.parent.joinpath(file_name)
            dir_path = file_path.parent if file_path.suffix else file_path
            dir_path.mkdir(exist_ok=True, parents=True)
        return file_path
