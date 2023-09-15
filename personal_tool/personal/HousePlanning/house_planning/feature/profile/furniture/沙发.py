from typing import Union

from ..base.furniture import Furniture


class Sofa(Furniture):

    def __init__(self, price: Union[int, float]):
        super().__init__("沙发", price)


class AboveFloorSofa(Sofa):

    def __init__(self, price: Union[int, float]):
        super().__init__(price)
        self.furniture_name = "地上沙发"
