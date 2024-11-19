import abc
import typing

from .....base.element_base import ElementBase
from ......file_feature import FileFeature
from ......volume_feature import VolumeFeature


class BossBulletBase(ElementBase, metaclass=abc.ABCMeta):

    def __init__(self, image_names: typing.List[str], speed: typing.Union[int, typing.Tuple[int, int]]):
        super().__init__(image_names)
        # 加载子弹音效
        self.sound = FileFeature.load_sound("game_scene/enemy/bullet/boss_attack.wav")
        # 设置子弹参数
        self.alive = False  # 存活
        self.invincible = False  # 无敌
        self.speed = speed  # 速度

    @abc.abstractmethod
    def move(self):
        """子弹移动"""

    def reset(self):
        """重置子弹"""
        self.alive = True
        self.invincible = True  # Boss子弹出现时，使其状态变为无敌，不触发碰撞效果
        # 播放子弹音效
        VolumeFeature.volume_play(self.sound)
