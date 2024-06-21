import random

from .base.boss_bullet_base import BossBulletBase
from .....setting.setting_feature import SettingFeature


class BossBullet04(BossBulletBase):

    def __init__(self):
        image_names = ["game_scene\\enemy\\bullet\\boss_bullet_04.png"]
        super().__init__(image_names, 0)

    def move(self):
        """子弹移动"""

    def reset(self):
        """重置子弹"""
        self.alive = True
        width, height = SettingFeature.screen_setting.screen_size
        self.rect.left = random.randint(0, width - self.rect.width)
        self.rect.top = random.randint(250, height - self.rect.height)
