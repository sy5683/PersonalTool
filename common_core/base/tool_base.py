import abc
import logging


class ToolBase(metaclass=abc.ABCMeta):
    """工具基类"""

    logging.basicConfig(level=logging.INFO,
                        format="[%(asctime)s]-%(levelname)s-%(filename)s(line:%(lineno)d): %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename=None,
                        filemode='a')
