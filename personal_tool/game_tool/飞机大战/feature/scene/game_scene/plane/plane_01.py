import typing

from .base.plane_base import PlaneBase


class Plane01(PlaneBase):

    def __init__(self, background_size: typing.Tuple[int, int], **kwargs):
        image_names = ["images\\game_scene\\plane\\plane_01.png"]
        super().__init__(image_names, background_size, **kwargs)
