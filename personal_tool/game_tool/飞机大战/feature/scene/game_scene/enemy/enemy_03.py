from .base.enemy_base import EnemyBase


class Enemy03(EnemyBase):

    def __init__(self):
        super().__init__("images\\game_scene\\enemy\\enemy_03.png", 10, 1)
