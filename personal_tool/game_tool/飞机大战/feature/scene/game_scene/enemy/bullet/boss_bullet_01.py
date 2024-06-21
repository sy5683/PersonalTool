import typing

from .base.boss_bullet_base import BossBulletBase
from .....setting.setting_feature import SettingFeature


class BossBullet01(BossBulletBase):

    def __init__(self, position: typing.Tuple[int, int]):
        image_names = ["game_scene\\enemy\\bullet\\boss_bullet_01.png"]
        super().__init__(image_names, 5)
        self.__position = position

    def move(self):
        """子弹移动"""
        self.rect.top += self.speed
        # 超过底部则子弹失效
        width, height = SettingFeature.screen_setting.screen_size
        if self.rect.top > height:
            self.alive = False

    def reset(self):
        """重置子弹"""
        self.alive = True
        self.rect.left, self.rect.top = self.__position
