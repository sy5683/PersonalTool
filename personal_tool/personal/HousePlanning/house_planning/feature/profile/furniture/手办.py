import typing

from ..base.furniture import Furniture


class GarageKits(Furniture):

    def __init__(self, price: typing.Union[int, float]):
        super().__init__("手办", price)


class LifeSizeGarageKits(GarageKits):

    def __init__(self, price: typing.Union[int, float]):
        super().__init__(price)
        self.furniture_name = "等身大手办"
