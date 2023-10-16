import typing

from ..base.furniture import Furniture


class Refrigerator(Furniture):

    def __init__(self, price: typing.Union[int, float]):
        super().__init__("冰箱", price)
