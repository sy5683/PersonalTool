import pygame

from .base.supply_base import SupplyBase
from ..plane.base.plane_base import PlaneBase
from ....file_feature import FileFeature
from ....volume_feature import VolumeFeature


class MedKitSupply(SupplyBase):

    def __init__(self):
        super().__init__("game_scene\\supply\\med_kit.png")
        # 加载补给音效
        self.sound = FileFeature.load_sound("game_scene\\supply\\get_med_kit.wav")  # 获取医疗包

    def trigger(self, plane: PlaneBase, **kwargs):
        """触发"""
        if pygame.sprite.collide_mask(self, plane):
            self.alive = False
            # 播放获取补给包音效
            VolumeFeature.volume_play(self.sound)
            # 增加飞机生命值
            plane.add_life_number()
