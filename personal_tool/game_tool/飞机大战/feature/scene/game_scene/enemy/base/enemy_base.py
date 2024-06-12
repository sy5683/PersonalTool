import abc
import random

import pygame

from .....file_feature import FileFeature
from .....setting.setting_feature import SettingFeature


class EnemyBase(pygame.sprite.Sprite, metaclass=abc.ABCMeta):

    def __init__(self, hit_points: int, speed: int, score: int, image_name: str, hit_image_name: str = ''):
        pygame.sprite.Sprite.__init__(self)
        # 读取敌机图片，mask函数将图片非透明部分设置为mask
        self.image = FileFeature.load_image(image_name)
        self.hit_image = FileFeature.load_image(hit_image_name) if hit_image_name else None
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        # 设置敌机参数
        self.hit = False  # 是否被击中
        self.hit_points = hit_points  # 生命值
        self.max_hit_points = hit_points  # 最大生命值
        self.score = score  # 分数
        self.speed = speed  # 速度

    def move(self):
        """敌机移动"""
        width, height = SettingFeature.screen_setting.screen_size
        if self.rect.top < height:
            self.rect.top += self.speed
        # 超过底部则重置敌机
        else:
            self.reset()

    def reset(self):
        """重置敌机"""
        self.hit_points = self.max_hit_points
        width, height = SettingFeature.screen_setting.screen_size
        self.rect.left, self.rect.top = random.randint(0, width - self.rect.width), random.randint(-5 * height, 0)
