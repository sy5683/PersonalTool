import abc
import typing

import pygame

from ...bullet.base.bullet_base import BulletBase
from ...bullet.bullet_01 import Bullet01
from ...bullet.bullet_02 import Bullet02
from ...bullet.bullet_03 import Bullet03
from .....file_feature import FileFeature
from .....setting.setting_feature import SettingFeature


class PlaneBase(pygame.sprite.Sprite, metaclass=abc.ABCMeta):

    def __init__(self, image_names: typing.List[str], bomb_number: int, life_number: int):
        pygame.sprite.Sprite.__init__(self)
        # 读取飞机图片，mask函数将图片非透明部分设置为mask
        self.images = self.__get_images(image_names)
        self.mask = None
        self.image = self.get_image()
        self.rect = self.image.get_rect()
        # 设置飞机参数
        self.active = True  # 存活
        self.bomb_number = bomb_number  # 炸弹数
        self.invincible = False  # 无敌
        self.level = 1  # 等级
        self.life_number = life_number  # 生命数
        self.shield = False  # 护盾
        self.speed = 10  # 速度
        # 初始化飞机
        self.reset()
        # 私有参数
        self.__max_bomb_number = bomb_number
        self.__max_life_number = life_number

    def add_bomb_number(self):
        """增加炸弹数"""
        self.bomb_number += 1
        # 当炸弹数为最大值时获得炸弹补给，则自动使用炸弹
        if self.bomb_number > self.__max_bomb_number:
            self.use_bomb()

    def add_life_number(self):
        """增加生命数"""
        if self.life_number < self.__max_life_number:
            self.life_number += 1
        else:
            # 当生命数为最大值时获得医疗包补给，则获得护盾
            self.shield = True

    def get_image(self):
        """获取图片"""
        self.image = next(self.images)
        self.mask = pygame.mask.from_surface(self.image)
        return self.image

    def get_bullets(self) -> typing.Generator[typing.List[BulletBase], None, None]:
        """根据等级获取子弹"""
        if self.level == 1:
            bullets = [Bullet01(self.rect.midtop)]
        elif self.level == 2:
            bullets = [
                Bullet02((self.rect.centerx - 33, self.rect.centery)),
                Bullet02((self.rect.centerx + 33, self.rect.centery))
            ]
        else:
            bullets = [
                Bullet03((self.rect.centerx - 33, self.rect.centery)),
                Bullet03(self.rect.midtop),
                Bullet03((self.rect.centerx + 33, self.rect.centery))
            ]
        while True:
            yield bullets

    def level_up(self):
        """升级"""
        if self.level < 3:
            self.level += 1
        else:
            # 当等级为最大值时获得升级补给，则短暂无敌、获得护盾并自动触发一个炸弹效果
            self.invincible = True
            self.shield = True
            self.bomb_number += 1
            self.use_bomb()

    def move(self):
        """飞机移动"""
        width, height = SettingFeature.screen_setting.screen_size
        key_pressed = pygame.key.get_pressed()
        if key_pressed[SettingFeature.key_setting.up_key]:
            self.rect.top = max(self.rect.top - self.speed, 0)
        if key_pressed[SettingFeature.key_setting.down_key]:
            self.rect.bottom = min(self.rect.bottom + self.speed, height)
        if key_pressed[SettingFeature.key_setting.left_key]:
            self.rect.left = max(self.rect.left - self.speed, 0)
        if key_pressed[SettingFeature.key_setting.right_key]:
            self.rect.right = min(self.rect.right + self.speed, width)

    def reset(self):
        """重置飞机"""
        self.active = True
        self.invincible = True
        self.level = 1
        width, height = SettingFeature.screen_setting.screen_size
        self.rect.left, self.rect.bottom = (width - self.rect.width) // 2, height

    def use_bomb(self):
        """使用炸弹"""
        if self.bomb_number:
            self.bomb_number -= 1
            # TODO
            print("使用炸弹")

    @staticmethod
    def __get_images(image_names) -> typing.Generator[pygame.Surface, None, None]:
        """获取图片迭代器"""
        while True:
            for image_name in image_names:
                yield FileFeature.load_image(image_name)
