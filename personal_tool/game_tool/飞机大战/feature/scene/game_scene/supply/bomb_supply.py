import pygame

from .base.supply_base import SupplyBase
from ..plane.base.plane_base import PlaneBase
from ....file_feature import FileFeature
from ....volume_feature import VolumeFeature


class BombSupply(SupplyBase):

    def __init__(self):
        super().__init__("game_scene\\supply\\bomb.png")
        self.music = FileFeature.load_sound("game_scene\\supply\\get_bomb.wav")

    def trigger(self, plane: PlaneBase):
        """触发"""
        if pygame.sprite.collide_mask(self, plane):
            self.active = False
            # 播放获取炸弹音效
            VolumeFeature.volume_play(self.music)
            # 增加飞机炸弹数
            plane.add_bomb_number()
