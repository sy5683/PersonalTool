from typing import Union

from ..base.furniture import Furniture


class Commode(Furniture):

    def __init__(self, price: Union[int, float]):
        super().__init__("马桶", price)
