import abc
import typing

import pygame

from .....file_feature import FileFeature
from .....setting.setting_feature import SettingFeature


class PlaneBase(pygame.sprite.Sprite, metaclass=abc.ABCMeta):

    def __init__(self, image_names: typing.List[str], background_size: typing.Tuple[int, int], **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.images = self.__get_images(image_names)
        # 背景参数变量本地化
        self.background_width, self.background_height = background_size[:2]
        # 设置飞机参数
        self.active = True  # 存活
        self.bomb_number = kwargs.get("bomb_number", 5)
        self.invincible = True  # 无敌，默认值为True说命飞机重生时无敌
        self.life_number = kwargs.get("life_number", 3)  # 生命数
        self.rect = self.get_image().get_rect()  # 坐标
        self.speed = 10  # 速度
        # 初始化飞机
        self.reset()

    def get_image(self):
        """获取图片"""
        image = next(self.images)
        # self.mask = pygame.mask.from_surface(image)
        return image

    def move(self):
        """飞机移动"""
        key_pressed = pygame.key.get_pressed()
        if key_pressed[SettingFeature.key_setting.up_key]:
            self.rect.top = max(self.rect.top - self.speed, 0)
        if key_pressed[SettingFeature.key_setting.down_key]:
            self.rect.bottom = min(self.rect.bottom + self.speed, self.background_height)
        if key_pressed[SettingFeature.key_setting.left_key]:
            self.rect.left = max(self.rect.left - self.speed, 0)
        if key_pressed[SettingFeature.key_setting.right_key]:
            self.rect.right = min(self.rect.right + self.speed, self.background_width)

    def reset(self):
        """重置飞机"""
        self.active = True
        self.invincible = True
        self.rect.left, self.rect.bottom = (self.background_width - self.rect.width) // 2, self.background_height

    @staticmethod
    def __get_images(image_names):
        """获取图片迭代器"""
        while True:
            for image_name in image_names:
                yield FileFeature.load_image(image_name)
