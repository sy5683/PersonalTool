import abc

import pygame
from PIL import Image

from ...setting.setting_feature import SettingFeature
from ...file_feature import FileFeature


class SceneBase(metaclass=abc.ABCMeta):

    def __init__(self, image_name: str, **kwargs):
        # 初始化刷新频率Clock
        self.clock = pygame.time.Clock()
        # 获取背景图片路径
        image_path = FileFeature.get_file_path(image_name)
        # 获取屏幕长宽
        SettingFeature.screen_setting.screen_size = Image.open(image_path).size[:2]
        # 设置窗口对象
        self.screen = self.get_screen()
        # 读取背景图片
        self.image = FileFeature.load_image(image_path)

    @abc.abstractmethod
    def main(self):
        """"""

    @staticmethod
    def get_screen(change_screen: bool = False) -> pygame.Surface:
        """获取窗口对象"""
        if change_screen:
            SettingFeature.screen_setting.full_screen = not SettingFeature.screen_setting.full_screen
        flags = pygame.FULLSCREEN | pygame.HWSURFACE if SettingFeature.screen_setting.full_screen else 0
        width, height = SettingFeature.screen_setting.screen_size
        return pygame.display.set_mode((width, height), flags)
