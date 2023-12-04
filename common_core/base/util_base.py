from .log_base import LogBase
import abc


class UtilBase(LogBase, metaclass=abc.ABCMeta):
    """组件基类"""
