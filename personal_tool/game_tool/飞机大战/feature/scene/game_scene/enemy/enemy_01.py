from .base.enemy_base import EnemyBase


class Enemy01(EnemyBase):

    def __init__(self):
        super().__init__("images\\game_scene\\enemy\\enemy_01.png", 1, 3)
