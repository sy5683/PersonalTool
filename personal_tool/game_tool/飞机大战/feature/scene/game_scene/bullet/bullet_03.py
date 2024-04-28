import typing

from .base.bullet_base import BulletBase


class Bullet03(BulletBase):

    def __init__(self, position: typing.Tuple[int, int]):
        super().__init__("images\\game_scene\\bullet\\bullet_03.png", 20, position)
