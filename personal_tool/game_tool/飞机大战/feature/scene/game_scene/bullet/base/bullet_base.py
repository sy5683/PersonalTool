import abc
import typing

import pygame

from .....file_feature import FileFeature
from .....volume_feature import VolumeFeature


class BulletBase(pygame.sprite.Sprite, metaclass=abc.ABCMeta):

    def __init__(self, image_name: str, speed: int, position: typing.Tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)
        # 读取子弹图片，mask函数将图片非透明部分设置为mask
        self.image = FileFeature.load_image(image_name)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        # 加载子弹音效
        self.sound = FileFeature.load_sound("game_scene\\bullet\\bullet.wav")
        # 设置子弹参数
        self.alive = False  # 存活
        self.speed = speed  # 速度
        self.rect.left, self.rect.top = position[0] - self.rect.width // 2, position[1]

    def attack_enemy(self, enemies):
        """子弹攻击敌机"""
        # 检测子弹是否击中敌机
        enemy_hit = pygame.sprite.spritecollide(self, enemies, False, pygame.sprite.collide_mask)
        if enemy_hit:
            self.alive = False
            for enemy in enemy_hit:
                enemy.hit = True
                enemy.hit_points -= 1

    def move(self):
        """子弹移动"""
        self.rect.bottom -= self.speed
        # 超过顶部则子弹失效
        if self.rect.bottom < 0:
            self.alive = False

    # 构造重置子弹的函数
    def reset(self):
        self.alive = True
        # 播放子弹音效
        VolumeFeature.volume_play(self.sound)
