import typing

from ..base.furniture import Furniture


class Commode(Furniture):

    def __init__(self, price: typing.Union[int, float]):
        super().__init__("马桶", price)
