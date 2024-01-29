import abc

from .log_base import LogBase


class ToolBase(LogBase, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def main(self, *args, **kwargs):
        """"""
