import typing

from .base.supply_base import SupplyBase


class BombSupply(SupplyBase):

    def __init__(self, background_size: typing.Tuple[int, int]):
        super().__init__("images\\game_scene\\supply\\bomb.png", background_size)
