import abc
import typing

import pygame

from ...cache.cache_feature import CacheFeature
from ...file_feature import FileFeature


class ElementBase(pygame.sprite.Sprite, metaclass=abc.ABCMeta):

    def __init__(self, image_names: typing.List[str]):
        pygame.sprite.Sprite.__init__(self)
        # 读取图片，mask函数将图片非透明部分设置为mask
        self.images = self._get_images(image_names)
        self.image = next(self.images)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

    def draw(self, screen: pygame.Surface):
        """绘制"""
        screen.blit(self.get_image(), self.rect)

    def get_image(self):
        """获取图片"""
        self.image = next(self.images) if CacheFeature.game_cache.delay % 10 == 0 else self.image
        self.mask = pygame.mask.from_surface(self.image)
        return self.image

    @staticmethod
    def _get_images(image_names: typing.List[str]) -> typing.Generator[pygame.Surface, None, None]:
        """获取图片迭代器"""
        while True:
            for image_name in image_names:
                yield FileFeature.get_image(image_name)
