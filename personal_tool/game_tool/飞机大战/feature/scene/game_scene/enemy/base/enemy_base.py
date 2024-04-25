import abc
import random

import pygame

from .....file_feature import FileFeature
from .....setting.setting_feature import SettingFeature


class EnemyBase(pygame.sprite.Sprite, metaclass=abc.ABCMeta):

    def __init__(self, image_name: str, energy: int, speed: int):
        pygame.sprite.Sprite.__init__(self)
        # 读取敌机图片，mask函数将图片非透明部分设置为mask
        self.image = FileFeature.load_image(image_name)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        # 设置敌机参数
        self.active = False  # 存活
        self.energy = energy  # 能源
        self.speed = speed  # 速度
        # 私有参数
        self.__max_energy = energy

    def move(self):
        """敌机移动"""
        width, height = SettingFeature.screen_setting.screen_size
        if self.rect.top < height:
            self.rect.top += self.speed
        # 超过底部则重置敌机
        else:
            self.reset()

    def reset(self):
        """重置敌机"""
        self.active = True
        self.energy = self.__max_energy
        width, height = SettingFeature.screen_setting.screen_size
        self.rect.left, self.rect.top = random.randint(0, width - self.rect.width), random.randint(-15 * height, height)
