from .base.enemy_base import EnemyBase


class Enemy01(EnemyBase):

    def __init__(self):
        image_names = ["game_scene\\enemy\\enemy_01\\enemy.png"]
        super().__init__(image_names, 1, 3, 100)
