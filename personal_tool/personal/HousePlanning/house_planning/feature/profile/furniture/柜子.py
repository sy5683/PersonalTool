import abc
import typing

from ..base.furniture import Furniture


class Cabinet(Furniture, metaclass=abc.ABCMeta):

    def __init__(self, furniture_name: str, price: typing.Union[int, float]):
        super().__init__(furniture_name, price)


class BedsideTable(Cabinet):

    def __init__(self, price: typing.Union[int, float]):
        super().__init__("床头柜", price)


class Showcase(Cabinet):

    def __init__(self, price: typing.Union[int, float]):
        super().__init__("展示柜", price)


class Wardrobe(Cabinet):

    def __init__(self, price: typing.Union[int, float]):
        super().__init__("衣柜", price)
