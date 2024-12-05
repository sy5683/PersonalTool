import abc
import typing


class InfoBase(metaclass=abc.ABCMeta):

    def __init__(self, info_name: str = None):
        self.info_name = info_name

    @abc.abstractmethod
    def to_contexts(self) -> typing.List[str]:
        """转换为文本"""
