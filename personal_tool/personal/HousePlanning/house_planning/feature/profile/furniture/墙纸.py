import typing

from ..base.furniture import Furniture


class Wallpaper(Furniture):

    def __init__(self, price: typing.Union[int, float]):
        super().__init__("墙纸", price)
