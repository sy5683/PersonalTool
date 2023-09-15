from typing import Union

from ..base.furniture import Furniture


class Shower(Furniture):

    def __init__(self, price: Union[int, float]):
        super().__init__("淋浴间", price)
