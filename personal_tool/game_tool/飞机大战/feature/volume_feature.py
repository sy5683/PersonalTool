import typing

import pygame

from .setting.setting_feature import SettingFeature


class VolumeFeature:

    @staticmethod
    def set_volume(volume: typing.Union[pygame.mixer.music, pygame.mixer.Sound]):
        """设置音量"""
        volume.set_volume(round(SettingFeature.volume_setting.main_volume / 100, 2))

    @classmethod
    def volume_play(cls, volume: pygame.mixer.Sound):
        """播放音效"""
        # 播放音效前先检测并设置音量
        cls.set_volume(volume)
        volume.play()
