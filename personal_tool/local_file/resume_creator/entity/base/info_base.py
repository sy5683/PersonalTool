from abc import ABCMeta, abstractmethod


class InfoBase(metaclass=ABCMeta):

    @abstractmethod
    def to_text(self) -> str:
        """转换为文本"""
