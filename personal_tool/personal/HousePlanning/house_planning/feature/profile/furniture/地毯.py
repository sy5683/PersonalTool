import typing

from ..base.furniture import Furniture


class Carpet(Furniture):

    def __init__(self, price: typing.Union[int, float]):
        super().__init__("地毯", price)


class GeothermalCarpet(Carpet):

    def __init__(self, price: typing.Union[int, float]):
        super().__init__(price)
        self.furniture_name = "地热毯"
