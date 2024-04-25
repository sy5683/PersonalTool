import abc

import pygame

from .....file_feature import FileFeature


class BackdropBase(pygame.sprite.Sprite, metaclass=abc.ABCMeta):

    def __init__(self, image_name: str):
        pygame.sprite.Sprite.__init__(self)
        # 读取背景图片，mask函数将图片非透明部分设置为mask
        self.image = FileFeature.load_image(image_name)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        # 设置背景参数
        self.active = False  # 存活

    @abc.abstractmethod
    def move(self):
        """背景移动"""

    @abc.abstractmethod
    def reset(self):
        """重置背景"""
