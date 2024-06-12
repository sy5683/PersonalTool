from .base.enemy_base import EnemyBase


class Enemy01(EnemyBase):

    def __init__(self):
        super().__init__(1, 3, 100, "game_scene\\enemy\\enemy_01.png")
