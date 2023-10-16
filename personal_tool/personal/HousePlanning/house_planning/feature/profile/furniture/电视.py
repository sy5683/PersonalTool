import typing

from ..base.furniture import Furniture


class Television(Furniture):

    def __init__(self, price: typing.Union[int, float]):
        super().__init__("电视", price)
