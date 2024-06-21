import abc
import random
import typing

import pygame

from ....base.element_base import ElementBase
from .....setting.setting_feature import SettingFeature


class EnemyBase(ElementBase, metaclass=abc.ABCMeta):

    def __init__(self, image_names: typing.List[str], hit_points: int, speed: typing.Union[int, typing.Tuple[int, int]],
                 score: int):
        super().__init__(image_names)
        # 设置敌机参数
        self.hit = False  # 是否被击中
        self.hit_points = hit_points  # 生命值
        self.score = score  # 分数
        self.speed = speed  # 速度
        # 私有参数
        self.__max_hit_points = hit_points  # 最大生命值

    def draw_crash(self, screen: pygame.Surface):
        """绘制坠毁"""
        # TODO 绘制坠毁动画

    def draw_hit_points_ratio(self, screen: pygame.Surface, top: int, width: int):
        """绘制血条"""
        hit_points_ratio = max(self.hit_points / self.__max_hit_points, 0)
        if hit_points_ratio < 1:
            pygame.draw.line(screen, (0, 0, 0), (self.rect.left, top), (self.rect.right, top), width)
            # 血量剩余20%显示绿色，否则显示红色
            color = (255, 0, 0) if hit_points_ratio < 0.2 else (0, 255, 0)
            right = self.rect.left + self.rect.width * hit_points_ratio
            pygame.draw.line(screen, color, (self.rect.left, top), (right, top), width)

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
        self.hit_points = self.__max_hit_points
        width, height = SettingFeature.screen_setting.screen_size
        self.rect.left, self.rect.top = random.randint(0, width - self.rect.width), random.randint(-5 * height, 0)
