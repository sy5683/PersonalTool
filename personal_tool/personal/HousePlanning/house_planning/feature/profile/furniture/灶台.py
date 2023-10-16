import typing

from ..base.furniture import Furniture


class CookingBench(Furniture):

    def __init__(self, price: typing.Union[int, float]):
        super().__init__("灶台", price)
