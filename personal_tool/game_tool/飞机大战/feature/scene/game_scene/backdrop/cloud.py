import random

from personal_tool.game_tool.飞机大战.feature.setting.setting_feature import SettingFeature
from .base.backdrop_base import BackdropBase


class Cloud(BackdropBase):

    def __init__(self):
        super().__init__("")  # TODO
        self.speed = 3  # 背景云朵速度

    def move(self):
        """背景云朵移动"""
        self.rect.top += self.speed
        # 超过底部则背景云朵失效
        width, height = SettingFeature.screen_setting.screen_size
        if self.rect.top > height:
            self.alive = False

    def reset(self):
        """重置背景云朵"""
        self.alive = True
        width, height = SettingFeature.screen_setting.screen_size
        self.rect.left, self.rect.bottom = random.randint(0, width - self.rect.width), -1
