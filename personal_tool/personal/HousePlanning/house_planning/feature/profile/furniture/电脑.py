from typing import Union

from ..base.furniture import Furniture


class Computer(Furniture):

    def __init__(self, price: Union[int, float]):
        super().__init__("电脑", price)
