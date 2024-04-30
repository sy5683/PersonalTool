import typing

from .base.bullet_base import BulletBase


class Bullet02(BulletBase):

    def __init__(self, position: typing.Tuple[int, int]):
        super().__init__("game_scene\\bullet\\bullet_02.png", 17, position)
