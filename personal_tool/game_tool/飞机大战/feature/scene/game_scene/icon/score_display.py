import pygame

from common_util.data_util.number_util.number_util import NumberUtil
from .base.icon_base import IconBase
from ....file_feature import FileFeature


class ScoreDisplay(IconBase):

    def __init__(self):
        super().__init__()
        self.font = FileFeature.get_font("font/fangsong_GB2312.ttf", 24)

    def draw(self, screen: pygame.Surface, score: int):
        """绘制得分"""
        text = f"Score: {NumberUtil.to_account(score)[:-3]}"
        screen.blit(self.font.render(text, True, (255, 255, 255)), (10, 10))
