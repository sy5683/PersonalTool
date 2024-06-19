import pygame

from common_util.data_util.number_util.number_util import NumberUtil
from .base.icon_base import IconBase
from ....file_feature import FileFeature


class ScoreIcon(IconBase):

    def __init__(self):
        super().__init__()
        self.font = FileFeature.load_font("font\\fangsong_GB2312.ttf", 24)

    def draw(self, screen: pygame.Surface, score: int):
        """绘制得分"""
        score_text = self.font.render(f"Score: {NumberUtil.to_account(score)[:-3]}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
