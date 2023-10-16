import typing

from ..base.furniture import Furniture


class Washer(Furniture):

    def __init__(self, price: typing.Union[int, float]):
        super().__init__("洗衣机", price)
