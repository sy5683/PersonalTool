from .profile.screen_config import ScreenConfig
from .profile.volume_config import VolumeConfig


class ConfigFeature:
    __screen_config = None
    __volume_config = None

    @classmethod
    def get_screen_config(cls) -> ScreenConfig:
        if cls.__screen_config is None:
            cls.__screen_config = ScreenConfig()
        return cls.__screen_config

    @classmethod
    def get_volume_config(cls) -> VolumeConfig:
        if cls.__volume_config is None:
            cls.__volume_config = VolumeConfig()
        return cls.__volume_config
