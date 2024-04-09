import typing

from .base.supply_base import SupplyBase


class StarSupply(SupplyBase):

    def __init__(self, background_size: typing.Tuple[int, int]):
        super().__init__("images\\game_scene\\supply\\star.png", background_size)
