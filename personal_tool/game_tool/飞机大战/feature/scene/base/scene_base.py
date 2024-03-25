import abc

import pygame
from PIL import Image

from ...config.config_feature import ConfigFeature
from ...file_feature import FileFeature


class SceneBase(metaclass=abc.ABCMeta):

    def __init__(self, background_name: str, **kwargs):
        # 设置刷新频率Clock
        self.clock = pygame.time.Clock()
        # 获取背景图片路径
        background_path = FileFeature.get_file_path(background_name)
        # 获取屏幕长宽
        self.width, self.height = Image.open(background_path).size
        # 设置窗口对象
        self.screen = self._update_screen()
        # 读取背景图片
        self.background_image = FileFeature.load_image(background_path)

    @abc.abstractmethod
    def main(self):
        """"""

    def _update_screen(self):
        screen_config = ConfigFeature.get_screen_config()
        self.screen = pygame.display.set_mode((self.width, self.height),
                                              pygame.FULLSCREEN | pygame.HWSURFACE if screen_config.full_screen else 0)
        return self.screen
