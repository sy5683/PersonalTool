import abc
import typing

from ....base.element_base import ElementBase
from .....file_feature import FileFeature
from .....volume_feature import VolumeFeature


class BulletBase(ElementBase, metaclass=abc.ABCMeta):

    def __init__(self, image_name: str, speed: int, position: typing.Tuple[int, int]):
        super().__init__([image_name])
        # 加载子弹音效
        self.sound = FileFeature.load_sound("game_scene\\bullet\\bullet.wav")
        # 设置子弹参数
        self.alive = False  # 存活
        self.speed = speed  # 速度
        self.rect.left, self.rect.top = position[0] - self.rect.width // 2, position[1]

    def move(self):
        """子弹移动"""
        self.rect.bottom -= self.speed
        # 超过顶部则子弹失效
        if self.rect.bottom < 0:
            self.alive = False

    # 构造重置子弹的函数
    def reset(self):
        self.alive = True
        # 播放子弹音效
        VolumeFeature.volume_play(self.sound)
