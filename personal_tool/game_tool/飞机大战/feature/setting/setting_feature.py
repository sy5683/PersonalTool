from .profile.game_setting import GameSetting
from .profile.key_setting import KeySetting
from .profile.screen_setting import ScreenSetting
from .profile.volume_setting import VolumeSetting


class SettingFeature:
    game_setting = GameSetting()
    key_setting = KeySetting()
    screen_setting = ScreenSetting()
    volume_setting = VolumeSetting()
