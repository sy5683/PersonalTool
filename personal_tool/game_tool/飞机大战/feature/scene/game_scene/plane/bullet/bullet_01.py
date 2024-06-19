import typing

from .base.bullet_base import BulletBase


class Bullet01(BulletBase):

    def __init__(self, position: typing.Tuple[int, int]):
        super().__init__("game_scene\\plane\\bullet\\bullet_01.png", 15, position)
