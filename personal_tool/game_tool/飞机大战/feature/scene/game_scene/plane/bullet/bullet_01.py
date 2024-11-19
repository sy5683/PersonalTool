import typing

from .base.plane_bullet_base import PlaneBulletBase


class PlaneBullet01(PlaneBulletBase):

    def __init__(self, position: typing.Tuple[int, int]):
        image_names = ["game_scene/plane/bullet/bullet_01.png"]
        super().__init__(image_names, 15, position)
