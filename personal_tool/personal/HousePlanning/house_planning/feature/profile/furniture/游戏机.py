import abc
import typing

from ..base.furniture import Furniture


class VideoGame(Furniture, metaclass=abc.ABCMeta):

    def __init__(self, furniture_name: str, price: typing.Union[int, float]):
        super().__init__(furniture_name, price)


class PS5(VideoGame):

    def __init__(self, price: typing.Union[int, float]):
        super().__init__("PS5", price)


class Switch(VideoGame):

    def __init__(self, price: typing.Union[int, float]):
        super().__init__("switch", price)
