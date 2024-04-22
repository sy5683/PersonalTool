import pygame

from .base.supply_base import SupplyBase
from ..plane.base.plane_base import PlaneBase


class BombSupply(SupplyBase):

    def __init__(self):
        super().__init__("images\\game_scene\\supply\\bomb.png")

    def trigger(self, plane: PlaneBase):
        """触发"""
        if pygame.sprite.collide_mask(self, plane):
            plane.add_bomb_number()
            self.active = False
