import math
import random
import typing

import pygame

from .base.boss_bullet_base import BossBulletBase
from .....cache.cache_feature import CacheFeature
from .....setting.setting_feature import SettingFeature


class BossBullet03(BossBulletBase):

    def __init__(self, position: typing.Tuple[int, int]):
        image_names = ["game_scene\\enemy\\bullet\\boss_bullet_03.png"]
        super().__init__(image_names, (0, 0))
        self.__position = position

    def draw(self, screen: pygame.Surface):
        """绘制子弹"""
        image = pygame.transform.rotate(self.get_image(), CacheFeature.game_cache.angle)
        screen.blit(image, self.rect)

    def move(self):
        """子弹移动"""
        self.rect = self.rect.move(self.speed)
        # 超过边缘转换子弹方向
        width, height = SettingFeature.screen_setting.screen_size
        if self.rect.left < 0 or self.rect.right > width:
            self.speed = (-self.speed[0], self.speed[1])
        if self.rect.top < 0 or self.rect.bottom > height:
            self.speed = (self.speed[0], -self.speed[1])

    def reset(self):
        """重置子弹"""
        super().reset()
        self.rect.left, self.rect.top = self.__position
        figure = random.randint(-5, 5)
        self.speed = (figure, 4 - int(math.fabs(figure)))
