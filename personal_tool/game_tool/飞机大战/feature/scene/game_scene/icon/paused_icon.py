import pygame

from .base.icon_base import IconBase
from ....file_feature import FileFeature
from ....setting.setting_feature import SettingFeature


class PauseIcon(IconBase):

    def __init__(self):
        super().__init__()
        self.image = FileFeature.load_image("game_scene/icon/pause.png")
        self.rect = self.image.get_rect()
        width, height = SettingFeature.screen_setting.screen_size
        self.rect.left = width - self.rect.width - 10
        self.rect.top = 10

    def draw(self, screen: pygame.Surface, pressed: bool):
        """绘制暂停按钮"""
        self.image.set_alpha(150 if pressed else 255)
        screen.blit(self.image, self.rect)
