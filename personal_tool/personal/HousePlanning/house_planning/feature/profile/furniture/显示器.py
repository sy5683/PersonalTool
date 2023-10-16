import abc
import typing

from ..base.furniture import Furniture


class Monitor(Furniture, metaclass=abc.ABCMeta):

    def __init__(self, furniture_name: str, price: typing.Union[int, float]):
        super().__init__(furniture_name, price)


class Projector(Monitor):

    def __init__(self, price: typing.Union[int, float]):
        super().__init__("投影仪", price)


class Television(Monitor):

    def __init__(self, price: typing.Union[int, float]):
        super().__init__("电视", price)
