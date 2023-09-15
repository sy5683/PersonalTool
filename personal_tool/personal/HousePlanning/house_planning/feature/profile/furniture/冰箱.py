from typing import Union

from ..base.furniture import Furniture


class Refrigerator(Furniture):

    def __init__(self, price: Union[int, float]):
        super().__init__("冰箱", price)
