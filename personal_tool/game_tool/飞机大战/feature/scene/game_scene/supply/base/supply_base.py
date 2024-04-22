import abc
import random

import pygame

from ...plane.base.plane_base import PlaneBase
from .....file_feature import FileFeature
from .....setting.setting_feature import SettingFeature


class SupplyBase(pygame.sprite.Sprite, metaclass=abc.ABCMeta):

    def __init__(self, image_name: str):
        pygame.sprite.Sprite.__init__(self)
        # 读取补给图片，mask函数将图片非透明部分设置为mask
        self.image = FileFeature.load_image(image_name)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        # 设置补给参数
        self.active = False  # 存活
        self.speed = 3  # 速度

    @abc.abstractmethod
    def trigger(self, plane: PlaneBase):
        """触发"""

    def move(self):
        """补给掉落"""
        width, height = SettingFeature.screen_setting.screen_size
        if self.rect.top < height:
            self.rect.top += self.speed
        # 超过底部则道具失效
        else:
            self.active = False

    def reset(self):
        """重置补给"""
        self.active = True
        width, height = SettingFeature.screen_setting.screen_size
        self.rect.left, self.rect.bottom = random.randint(0, width - self.rect.width), -1
