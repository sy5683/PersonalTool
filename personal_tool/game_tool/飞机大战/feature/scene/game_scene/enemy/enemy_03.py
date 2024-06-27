import pygame

from .base.enemy_base import EnemyBase
from ....file_feature import FileFeature


class Enemy03(EnemyBase):

    def __init__(self):
        image_names = ["game_scene\\enemy\\enemy_03\\enemy_1.png", "game_scene\\enemy\\enemy_03\\enemy_2.png"]
        super().__init__(image_names, 10, 1, 5000)

    def draw(self, screen: pygame.Surface):
        """绘制敌机"""
        # TODO hit图片需要做到叠加，而不是替换
        hit_image = FileFeature.load_image("game_scene\\enemy\\enemy_03\\enemy_hit.png")
        screen.blit(hit_image if self.hit else self.get_image(), self.rect)
        self.draw_hit_points_ratio(screen, self.rect.top - 5, 3)
        self.hit = False
