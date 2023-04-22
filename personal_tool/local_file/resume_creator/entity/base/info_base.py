from abc import ABCMeta, abstractmethod


class InfoBase(metaclass=ABCMeta):

    def __init__(self, info_name: str = None):
        self.info_name = info_name

    @abstractmethod
    def to_text(self) -> str:
        """转换为文本"""
