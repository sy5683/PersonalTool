from abc import ABCMeta
from typing import Union

from ..base.furniture import Furniture


class Monitor(Furniture, metaclass=ABCMeta):

    def __init__(self, furniture_name: str, price: Union[int, float]):
        super().__init__(furniture_name, price)


class Projector(Monitor):

    def __init__(self, price: Union[int, float]):
        super().__init__("投影仪", price)


class Television(Monitor):

    def __init__(self, price: Union[int, float]):
        super().__init__("电视", price)
