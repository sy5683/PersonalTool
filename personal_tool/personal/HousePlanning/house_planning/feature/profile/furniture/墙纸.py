from typing import Union

from ..base.furniture import Furniture


class Wallpaper(Furniture):

    def __init__(self, price: Union[int, float]):
        super().__init__("墙纸", price)
