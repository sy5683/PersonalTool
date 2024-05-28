from .base.enemy_base import EnemyBase


class Enemy01(EnemyBase):

    def __init__(self):
        super().__init__("game_scene\\enemy\\enemy_01.png", 1, 3, 100)
