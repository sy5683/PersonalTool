import typing

from ..base.furniture import Furniture


class Shower(Furniture):

    def __init__(self, price: typing.Union[int, float]):
        super().__init__("淋浴间", price)
