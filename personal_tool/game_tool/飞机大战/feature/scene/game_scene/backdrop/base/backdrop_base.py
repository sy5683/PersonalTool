import abc

from ....base.element_base import ElementBase


class BackdropBase(ElementBase, metaclass=abc.ABCMeta):

    def __init__(self, image_name: str):
        super().__init__([image_name])
        # 设置背景参数
        self.alive = False  # 存活

    @abc.abstractmethod
    def move(self):
        """背景移动"""

    @abc.abstractmethod
    def reset(self):
        """重置背景"""
