from .base.enemy_base import EnemyBase


class Enemy02(EnemyBase):

    def __init__(self):
        super().__init__("images\\game_scene\\enemy\\enemy_02.png", 5, 2)
