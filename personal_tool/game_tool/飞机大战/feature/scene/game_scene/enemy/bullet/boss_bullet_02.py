import typing

import pygame

from .base.boss_bullet_base import BossBulletBase
from .....cache.cache_feature import CacheFeature
from .....setting.setting_feature import SettingFeature


class BossBullet02(BossBulletBase):

    def __init__(self, speeds: typing.Tuple[int, int]):
        image_names = ["game_scene\\enemy\\bullet\\boss_bullet_02.png"]
        super().__init__(image_names, speeds)

    def draw(self, screen: pygame.Surface):
        """绘制子弹"""
        image = pygame.transform.rotate(self.get_image(), CacheFeature.game_cache.angle)
        screen.blit(image, self.rect)

    def move(self):
        """子弹移动"""
        self.rect = self.rect.move(self.speed)
        # 超过边缘则子弹失效
        width, height = SettingFeature.screen_setting.screen_size
        if self.rect.left > width or self.rect.right < 0 or self.rect.top > height:
            self.alive = False

    def reset(self):
        """重置子弹"""
        super().reset()
        width, height = SettingFeature.screen_setting.screen_size
        self.rect.left, self.rect.top = (width - self.rect.width) // 2, 100
