from typing import Union

from ..base.furniture import Furniture


class Toilet(Furniture):

    def __init__(self, price: Union[int, float]):
        super().__init__("厕所", price)
