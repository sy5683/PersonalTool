from .base.enemy_base import EnemyBase


class Enemy03(EnemyBase):

    def __init__(self):
        super().__init__(10, 1, 5000, "game_scene\\enemy\\enemy_03.png", "game_scene\\enemy\\enemy_03_hit.png")
