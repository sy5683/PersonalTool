import typing

from .base.plane_base import PlaneBase


class Player1Plane(PlaneBase):

    def __init__(self, background_size: typing.Tuple[int, int]):
        super().__init__("images\\game_scene\\plane\\player1.png", background_size)

    def reset(self):
        super().reset()
        self.rect.left, self.rect.bottom = (self.background_width - self.rect.width) // 2, self.background_height
