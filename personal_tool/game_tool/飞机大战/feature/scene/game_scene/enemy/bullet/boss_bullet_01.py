import typing

import pygame

from .base.boss_bullet_base import BossBulletBase
from .....cache.cache_feature import CacheFeature
from .....setting.setting_feature import SettingFeature


class BossBullet01(BossBulletBase):

    def __init__(self, position: typing.Tuple[int, int]):
        image_names = ["game_scene\\enemy\\bullet\\boss_bullet_01.png"]
        super().__init__(image_names, 5)
        self.__position = position

    def draw(self, screen: pygame.Surface):
        """绘制子弹"""
        angle = CacheFeature.game_cache.delay // 25 * 90
        image = pygame.transform.rotate(self.get_image(), angle)
        screen.blit(image, self.rect)

    def move(self):
        """子弹移动"""
        self.rect.top += self.speed
        # 超过底部则子弹失效
        width, height = SettingFeature.screen_setting.screen_size
        if self.rect.top > height:
            self.alive = False

    def reset(self):
        """重置子弹"""
        super().reset()
        self.rect.left, self.rect.top = self.__position
