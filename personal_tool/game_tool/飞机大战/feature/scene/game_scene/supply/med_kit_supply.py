from .base.supply_base import SupplyBase
from ..plane.base.plane_base import PlaneBase
from ....file_feature import FileFeature
from ....volume_feature import VolumeFeature


class MedKitSupply(SupplyBase):

    def __init__(self):
        super().__init__("game_scene\\supply\\med_kit\\med_kit.png")
        # 加载补给音效
        self.sound = FileFeature.load_sound("game_scene\\supply\\med_kit\\get_med_kit.wav")  # 获取医疗包

    def trigger(self, plane: PlaneBase, enemies):
        """触发"""
        self.alive = False
        # 播放获取补给包音效
        VolumeFeature.volume_play(self.sound)
        # 增加飞机生命值
        plane.add_life_number()
