import abc
import logging


class LogBase(metaclass=abc.ABCMeta):
    """日志基类"""

    logging.basicConfig(level=logging.INFO,
                        format="[%(asctime)s]-%(levelname)s-%(filename)s(line:%(lineno)d): %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename=None,
                        filemode='a')
