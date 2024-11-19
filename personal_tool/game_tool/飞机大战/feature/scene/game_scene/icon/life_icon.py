import pygame

from .base.icon_base import IconBase
from ....file_feature import FileFeature
from ....setting.setting_feature import SettingFeature


class LifeIcon(IconBase):

    def __init__(self):
        super().__init__()
        self.image = FileFeature.load_image("game_scene/icon/life.png")
        self.rect = self.image.get_rect()

    def draw(self, screen: pygame.Surface, life_number: int):
        """绘制生命值"""
        width, height = SettingFeature.screen_setting.screen_size
        for index in range(life_number):
            screen.blit(self.image, (index * self.rect.width, height - self.rect.height - 10))
