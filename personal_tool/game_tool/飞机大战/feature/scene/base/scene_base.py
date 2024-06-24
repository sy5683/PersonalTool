import abc

import pygame
from PIL import Image

from ...setting.setting_feature import SettingFeature
from ...file_feature import FileFeature


class SceneBase(metaclass=abc.ABCMeta):

    def __init__(self, image_name: str, music_name: str, **kwargs):
        # 初始化刷新频率Clock
        self.clock = pygame.time.Clock()
        # 获取背景图片路径
        image_path = FileFeature.get_file_path(image_name)
        # 获取屏幕长宽
        width, height = Image.open(image_path).size[:2]
        SettingFeature.screen_setting.screen_size = width, height // 2
        # 设置窗口对象
        self.screen = self.get_screen()
        # 读取背景图片
        self.image = FileFeature.load_image(image_path)
        # 加载背景音乐
        FileFeature.load_music(music_name)
        # 背景参数
        self.rect = self.image.get_rect()
        self.speed = 1  # 速度
        # 功能参数
        self.running = True  # 判断运行
        # 初始化背景
        self.reset()
        # 私有参数
        self.__timer_index = 0

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

    def move(self):
        """背景移动"""
        self.rect.top += self.speed
        if self.rect.top >= 0:
            self.reset()

    def reset(self):
        """重置背景"""
        width, height = SettingFeature.screen_setting.screen_size
        self.rect.top = -height

    def get_timer(self, seconds: int = None) -> int:
        """获取计时器"""
        timer = pygame.USEREVENT + self.__timer_index
        if seconds:
            pygame.time.set_timer(timer, seconds * 1000)
        self.__timer_index += 1
        return timer
