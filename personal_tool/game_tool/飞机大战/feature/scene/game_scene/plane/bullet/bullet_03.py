import typing

from .base.plane_bullet_base import PlaneBulletBase


class PlaneBullet03(PlaneBulletBase):

    def __init__(self, position: typing.Tuple[int, int]):
        image_names = ["game_scene/plane\\bullet\\bullet_03.png"]
        super().__init__(image_names, 20, position)
