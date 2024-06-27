import pygame

from .base.enemy_base import EnemyBase
from ....file_feature import FileFeature


class Enemy02(EnemyBase):

    def __init__(self):
        image_names = ["game_scene\\enemy\\enemy_02\\enemy.png"]
        super().__init__(image_names, 5, 2, 1000)

    def draw(self, screen: pygame.Surface):
        """绘制敌机"""
        hit_image = FileFeature.load_image("game_scene\\enemy\\enemy_02\\enemy_hit.png")
        screen.blit(hit_image if self.hit else self.get_image(), self.rect)
        self.draw_hit_points_ratio(screen, self.rect.top - 5, 2)
        self.hit = False
