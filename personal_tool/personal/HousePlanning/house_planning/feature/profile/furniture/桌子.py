from abc import ABCMeta
from typing import Union

from ..base.furniture import Furniture


class Table(Furniture, metaclass=ABCMeta):

    def __init__(self, furniture_name: str, price: Union[int, float]):
        super().__init__(furniture_name, price)


class Board(Table):

    def __init__(self, price: Union[int, float]):
        super().__init__("餐桌", price)


class ComputerDesk(Table):

    def __init__(self, price: Union[int, float]):
        super().__init__("电脑桌", price)


class TeaTable(Table):

    def __init__(self, price: Union[int, float]):
        super().__init__("茶几", price)


class ToiletTable(Table):

    def __init__(self, price: Union[int, float]):
        super().__init__("洗漱台", price)


class WritingDesk(Table):

    def __init__(self, price: Union[int, float]):
        super().__init__("书桌", price)
