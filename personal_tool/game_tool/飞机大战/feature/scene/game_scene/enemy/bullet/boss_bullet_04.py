import random

import pygame

from .base.boss_bullet_base import BossBulletBase
from .....cache.cache_feature import CacheFeature
from .....setting.setting_feature import SettingFeature


class BossBullet04(BossBulletBase):

    def __init__(self):
        image_names = ["game_scene/enemy/bullet/boss_bullet_04.png"]
        super().__init__(image_names, 0)

    def draw(self, screen: pygame.Surface):
        """绘制子弹"""
        image = self.get_image()
        if CacheFeature.game_cache.delay % 50 < 25:
            image.set_alpha(255 - (CacheFeature.game_cache.delay % 50) * 4)
        else:
            image.set_alpha(255 - (-CacheFeature.game_cache.delay % 50) * 4)
        screen.blit(image, self.rect)

    def move(self):
        """子弹移动"""

    def reset(self):
        """重置子弹"""
        super().reset()
        width, height = SettingFeature.screen_setting.screen_size
        self.rect.left = random.randint(0, width - self.rect.width)
        self.rect.top = random.randint(250, height - self.rect.height)
