import typing

from ..base.furniture import Furniture


class Toilet(Furniture):

    def __init__(self, price: typing.Union[int, float]):
        super().__init__("厕所", price)
