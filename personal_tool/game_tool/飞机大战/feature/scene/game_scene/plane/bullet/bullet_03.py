import typing

from .base.bullet_base import BulletBase


class Bullet03(BulletBase):

    def __init__(self, position: typing.Tuple[int, int]):
        super().__init__("game_scene\\plane\\bullet\\bullet_03.png", 20, position)
