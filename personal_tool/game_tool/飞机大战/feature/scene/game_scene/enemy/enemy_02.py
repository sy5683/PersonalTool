from .base.enemy_base import EnemyBase


class Enemy02(EnemyBase):

    def __init__(self):
        super().__init__("game_scene\\enemy\\enemy_02.png", 5, 2, 1000)
