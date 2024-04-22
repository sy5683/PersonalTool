import pygame

from .base.supply_base import SupplyBase
from ..plane.base.plane_base import PlaneBase


class MedKitSupply(SupplyBase):

    def __init__(self):
        super().__init__("images\\game_scene\\supply\\med_kit.png")

    def trigger(self, plane: PlaneBase):
        """触发"""
        if pygame.sprite.collide_mask(self, plane):
            plane.add_life_number()
            self.active = False
