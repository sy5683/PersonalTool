import abc

from .log_base import LogBase


class ToolBase(LogBase, metaclass=abc.ABCMeta):
    """工具基类"""

    @abc.abstractmethod
    def main(self, *args, **kwargs):
        """"""
