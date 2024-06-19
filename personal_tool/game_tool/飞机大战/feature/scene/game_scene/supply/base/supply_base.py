import abc
import random

from ...plane.base.plane_base import PlaneBase
from ....base.element_base import ElementBase
from .....file_feature import FileFeature
from .....setting.setting_feature import SettingFeature
from .....volume_feature import VolumeFeature


class SupplyBase(ElementBase, metaclass=abc.ABCMeta):

    def __init__(self, image_name: str):
        super().__init__([image_name])
        # 加载补给音效
        self.appear_sound = FileFeature.load_sound("game_scene\\supply\\appear.wav")  # 补给出现
        # 设置补给参数
        self.alive = False  # 存活
        self.speed = 3  # 速度

    @abc.abstractmethod
    def trigger(self, plane: PlaneBase, enemies):
        """触发"""

    def move(self):
        """补给掉落"""
        self.rect.top += self.speed
        # 超过底部则道具失效
        width, height = SettingFeature.screen_setting.screen_size
        if self.rect.top > height:
            self.alive = False

    def reset(self):
        """重置补给"""
        self.alive = True
        # 随机生成出现坐标
        width, height = SettingFeature.screen_setting.screen_size
        self.rect.left, self.rect.bottom = random.randint(0, width - self.rect.width), -1
        # 播放补给出现音效
        VolumeFeature.volume_play(self.appear_sound)
