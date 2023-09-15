from typing import Union

from ..base.furniture import Furniture


class Bed(Furniture):

    def __init__(self, price: Union[int, float]):
        super().__init__("床", price)
