import abc
import random
import typing

import pygame

from .....file_feature import FileFeature


class SupplyBase(pygame.sprite.Sprite, metaclass=abc.ABCMeta):

    def __init__(self, image_name: str, background_size: typing.Tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)
        # 读取补给图片，mask函数将图片非透明部分设置为mask
        self.image = FileFeature.load_image(image_name)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        # 背景参数变量本地化
        self.background_width, self.background_height = background_size[:2]
        # 设置补给参数
        self.active = False  # 存活
        self.speed = 3  # 速度
        # 初始化补给
        self.reset()

    def move(self):
        """补给掉落"""
        if self.rect.top < self.background_height:
            self.rect.top += self.speed
        # 超过底部则道具失效
        else:
            self.active = False

    def reset(self):
        """重置补给"""
        self.active = True
        self.rect.left, self.rect.bottom = random.randint(0, self.background_width - self.rect.width), -1
