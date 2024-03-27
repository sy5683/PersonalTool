from .profile.key_setting import KeySetting
from .profile.screen_setting import ScreenSetting
from .profile.volume_setting import VolumeSetting


class SettingFeature:
    __key_setting = None
    __screen_setting = None
    __volume_setting = None

    @classmethod
    def get_key_setting(cls) -> KeySetting:
        if cls.__key_setting is None:
            cls.__key_setting = KeySetting()
        return cls.__key_setting

    @classmethod
    def get_screen_setting(cls) -> ScreenSetting:
        if cls.__screen_setting is None:
            cls.__screen_setting = ScreenSetting()
        return cls.__screen_setting

    @classmethod
    def get_volume_setting(cls) -> VolumeSetting:
        if cls.__volume_setting is None:
            cls.__volume_setting = VolumeSetting()
        return cls.__volume_setting
