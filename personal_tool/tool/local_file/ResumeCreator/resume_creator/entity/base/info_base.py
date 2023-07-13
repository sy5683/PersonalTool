from abc import ABCMeta, abstractmethod
from typing import List


class InfoBase(metaclass=ABCMeta):

    def __init__(self, info_name: str = None):
        self.info_name = info_name

    @abstractmethod
    def to_contexts(self) -> List[str]:
        """转换为文本"""
