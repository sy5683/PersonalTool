from .base.backdrop_base import BackdropBase
from ....setting.setting_feature import SettingFeature


class Airport(BackdropBase):

    def __init__(self):
        super().__init__("game_scene\\backdrop\\airport.png")
        self.speed = 3  # 背景起飞坪速度

    def move(self):
        """背景起飞坪移动"""
        self.rect.top += self.speed
        # 超过底部则背景起飞坪失效
        width, height = SettingFeature.screen_setting.screen_size
        if self.rect.top > height:
            self.alive = False

    def reset(self):
        """重置背景起飞坪"""
        self.alive = True
        width, height = SettingFeature.screen_setting.screen_size
        self.rect.left, self.rect.bottom = (width - self.rect.width) // 2,  height
