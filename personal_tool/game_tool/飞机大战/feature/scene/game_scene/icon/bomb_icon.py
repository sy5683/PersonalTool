import pygame

from .base.icon_base import IconBase
from ....file_feature import FileFeature
from ....setting.setting_feature import SettingFeature


class BombIcon(IconBase):

    def __init__(self):
        super().__init__()
        self.font = FileFeature.get_font("font\\boldface.ttf", 20)
        self.image = FileFeature.get_image("game_scene\\icon\\bomb.png")
        self.rect = self.image.get_rect()
        width, height = SettingFeature.screen_setting.screen_size
        self.rect.left = width - self.rect.width
        self.rect.top = height - self.rect.height - 10

    def draw(self, screen: pygame.Surface, bomb_number: int):
        """绘制炸弹数"""
        self.image.set_alpha(255 if bomb_number else 150)
        screen.blit(self.image, self.rect)
        bomb_text = self.font.render(str(bomb_number), True, (255, 255, 255))
        screen.blit(bomb_text, (self.rect.left + 45, self.rect.top + 30))
