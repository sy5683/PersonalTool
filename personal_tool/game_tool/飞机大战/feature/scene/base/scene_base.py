import abc

import pygame
from PIL import Image

from ...config.config_feature import ConfigFeature
from ...file_feature import FileFeature


class SceneBase(metaclass=abc.ABCMeta):

    def __init__(self, image_name: str, **kwargs):
        # 初始化刷新频率Clock
        self.clock = pygame.time.Clock()
        # 获取背景图片路径
        image_path = FileFeature.get_file_path(image_name)
        # 获取屏幕长宽
        self.width, self.height = Image.open(image_path).size
        # 设置窗口对象
        self.screen = self.get_screen()
        # 读取背景图片
        self.image = FileFeature.load_image(image_path)

    @abc.abstractmethod
    def main(self):
        """"""

    def get_screen(self, change_screen: bool = False) -> pygame.Surface:
        """获取窗口对象"""
        screen_config = ConfigFeature.get_screen_config()
        if change_screen:
            screen_config.full_screen = not screen_config.full_screen
        flags = pygame.FULLSCREEN | pygame.HWSURFACE if screen_config.full_screen else 0
        return pygame.display.set_mode((self.width, self.height), flags if screen_config.full_screen else 0)
