import pygame

from .base.enemy_base import EnemyBase
from ....file_feature import FileFeature


class Boss(EnemyBase):

    def __init__(self):
        image_names = ["game_scene\\enemy\\boss.png",
                       "game_scene\\enemy\\boss_2.png",
                       "game_scene\\enemy\\boss_3.png",
                       "game_scene\\enemy\\boss_4.png"]
        super().__init__(image_names, 10000, 1, 1000000)
        # 设置Boss初始位置
        self.rect.left, self.rect.top = 0, -250

    def draw(self, screen: pygame.Surface):
        """绘制Boss"""
        # TODO hit图片需要做到叠加，而不是替换
        hit_image = FileFeature.get_image("game_scene\\enemy\\boss_hit.png")
        screen.blit(hit_image if self.hit else self.get_image(), self.rect)
        self.draw_hit_points_ratio(screen, 10, 5)
        self.hit = False

    def move(self):
        """Boss移动"""
        self.rect.top += self.speed if self.rect.top < 0 else 0
