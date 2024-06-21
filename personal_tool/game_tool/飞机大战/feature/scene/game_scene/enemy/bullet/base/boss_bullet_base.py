import abc
import typing

from .....base.element_base import ElementBase


class BossBulletBase(ElementBase, metaclass=abc.ABCMeta):

    def __init__(self, image_names: typing.List[str], speed: typing.Union[int, typing.Tuple[int, int]]):
        super().__init__(image_names)
        # 设置子弹参数
        self.alive = False  # 存活
        self.speed = speed  # 速度

    @abc.abstractmethod
    def move(self):
        """子弹移动"""

    @abc.abstractmethod
    def reset(self):
        """重置子弹"""
