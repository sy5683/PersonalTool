from typing import Union

from ..base.furniture import Furniture


class Kitchenware(Furniture):

    def __init__(self, price: Union[int, float]):
        super().__init__("厨具", price)


class MicrowaveOven(Kitchenware):

    def __init__(self, price: Union[int, float]):
        super().__init__(price)
        self.furniture_name = "微波炉"


class Oven(Kitchenware):

    def __init__(self, price: Union[int, float]):
        super().__init__(price)
        self.furniture_name = "烤箱"
