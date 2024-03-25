import abc

import pygame
from PIL import Image

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
        self.screen = pygame.display.set_mode((self.width, self.height))
        # 读取背景图片
        self.background_image = FileFeature.load_image(background_path)

    @abc.abstractmethod
    def main(self):
        """"""
