import pygame

from .base.icon_base import IconBase
from ....file_feature import FileFeature
from ....setting.setting_feature import SettingFeature


class Life(IconBase):

    def __init__(self):
        super().__init__()
        self.image = FileFeature.get_image("game_scene\\icon\\life.png")
        self.rect = self.image.get_rect()

    def draw(self, screen: pygame.Surface, life_num: int):
        """绘制生命值"""
        width, height = SettingFeature.screen_setting.screen_size
        for index in range(life_num):
            screen.blit(self.image, (index * self.rect.width, height - 10 - self.rect.height))
