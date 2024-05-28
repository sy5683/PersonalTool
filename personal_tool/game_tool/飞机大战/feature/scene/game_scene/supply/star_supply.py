import pygame

from .base.supply_base import SupplyBase
from ..plane.base.plane_base import PlaneBase
from ....file_feature import FileFeature
from ....volume_feature import VolumeFeature


class StarSupply(SupplyBase):

    def __init__(self):
        super().__init__("game_scene\\supply\\star.png")
        # 加载补给音效
        self.sound = FileFeature.load_sound("game_scene\\supply\\get_star.wav")  # 获取星星

    def trigger(self, plane: PlaneBase, **kwargs):
        """触发"""
        if pygame.sprite.collide_mask(self, plane):
            self.alive = False
            # 播放获取星星音效
            VolumeFeature.volume_play(self.sound)
            # 飞机升级
            enemies = kwargs.get("enemies", [])
            plane.level_up(enemies)
