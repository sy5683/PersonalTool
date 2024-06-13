from .base.plane_base import PlaneBase


class Plane01(PlaneBase):

    def __init__(self, bomb_number: int, life_number: int):
        image_names = ["game_scene\\plane\\plane_01.png"]
        super().__init__(image_names, bomb_number, life_number)
