import abc
import typing

import pygame

from .....file_feature import FileFeature
from .....setting.setting_feature import SettingFeature


class PlaneBase(pygame.sprite.Sprite, metaclass=abc.ABCMeta):

    def __init__(self, image_name: str, background_size: typing.Tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)
        # 读取飞机图片，mask函数将图片非透明部分设置为mask
        self.image = FileFeature.load_image(image_name)
        self.mask = pygame.mask.from_surface(self.image)
        # 背景参数变量本地化
        self.background_width, self.background_height = background_size[:2]
        # 设置飞机参数
        self.rect = self.image.get_rect()  # 坐标
        self.speed = 10  # 速度
        self.active = True  # 存活
        self.invincible = True  # 无敌，默认值为True说命飞机重生时无敌
        # 重置飞机
        self.reset()

    def move(self):
        """飞机移动"""
        key_pressed = pygame.key.get_pressed()
        key_setting = SettingFeature.get_key_setting()
        if key_pressed[key_setting.up_key]:
            self.rect.top = max(self.rect.top - self.speed, 0)
        if key_pressed[key_setting.down_key]:
            self.rect.bottom = min(self.rect.bottom + self.speed, self.background_height)
        if key_pressed[key_setting.left_key]:
            self.rect.left = max(self.rect.left - self.speed, 0)
        if key_pressed[key_setting.right_key]:
            self.rect.right = min(self.rect.right + self.speed, self.background_width)

    def reset(self):
        """重置飞机"""
        self.active = True
        self.invincible = True
        self.rect.left, self.rect.bottom = (self.background_width - self.rect.width) // 2, self.background_height
