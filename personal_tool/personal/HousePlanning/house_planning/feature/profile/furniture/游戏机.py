from abc import ABCMeta
from typing import Union

from ..base.furniture import Furniture


class VideoGame(Furniture, metaclass=ABCMeta):

    def __init__(self, furniture_name: str, price: Union[int, float]):
        super().__init__(furniture_name, price)


class PS5(VideoGame):

    def __init__(self, price: Union[int, float]):
        super().__init__("PS5", price)


class Switch(VideoGame):

    def __init__(self, price: Union[int, float]):
        super().__init__("switch", price)
