import typing

from .base.plane_base import PlaneBase


class Plane01(PlaneBase):

    def __init__(self, background_size: typing.Tuple[int, int]):
        super().__init__("images\\game_scene\\plane\\plane_01.png", background_size)
