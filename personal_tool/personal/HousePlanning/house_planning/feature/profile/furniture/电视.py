from typing import Union

from ..base.furniture import Furniture


class Television(Furniture):

    def __init__(self, price: Union[int, float]):
        super().__init__("电视", price)
