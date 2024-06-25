import abc
import typing

import pygame

from ..bullet.base.plane_bullet_base import PlaneBulletBase
from ..bullet.bullet_01 import PlaneBullet01
from ..bullet.bullet_02 import PlaneBullet02
from ..bullet.bullet_03 import PlaneBullet03
from ...enemy.base.enemy_base import EnemyBase
from ....base.element_base import ElementBase
from .....cache.cache_feature import CacheFeature
from .....file_feature import FileFeature
from .....setting.setting_feature import SettingFeature
from .....volume_feature import VolumeFeature


class PlaneBase(ElementBase, metaclass=abc.ABCMeta):

    def __init__(self, image_names: typing.List[str], bomb_number: int, life_number: int):
        super().__init__(image_names)
        # 加载飞机音效
        self.upgrade_sound = FileFeature.load_sound("game_scene\\plane\\upgrade.wav")  # 飞机升级
        # 设置飞机参数
        self.alive = True  # 存活
        self.bomb_number = bomb_number  # 炸弹数
        self.bullets: typing.List[PlaneBulletBase] = []
        self.invincible = False  # 无敌
        self.level = 1  # 等级
        self.life_number = life_number  # 生命数
        self.shield = False  # 护盾
        self.speed = 10  # 速度
        # 私有参数
        self.__max_bomb_number = bomb_number
        self.__max_life_number = life_number
        self.__switch_invincible = True

    def add_bomb_number(self, enemies):
        """增加炸弹数"""
        self.bomb_number += 1
        # 当炸弹数为最大值时获得炸弹补给，则自动使用炸弹
        if self.bomb_number > self.__max_bomb_number:
            self.use_bomb(enemies)

    def add_life_number(self):
        """增加生命数"""
        if self.life_number < self.__max_life_number:
            self.life_number += 1
        else:
            # 当生命数为最大值时获得医疗包补给，则获得护盾
            self.shield = True

    def crash(self):
        """飞机坠毁"""
        if self.shield:
            self.shield = False
        else:
            self.alive = False
            self.life_number -= 1

    def draw(self, screen: pygame.Surface):
        """绘制飞机"""
        # 实现飞机无敌时的闪烁特效
        if self.invincible and CacheFeature.game_cache.delay % 20 < 10:
            return
        screen.blit(self.get_image(), self.rect)

    def draw_crash(self, screen: pygame.Surface):
        """绘制飞机坠毁"""
        # TODO 绘制坠毁动画

    def get_bullets(self) -> typing.List[PlaneBulletBase]:
        """获取子弹"""
        # 添加子弹到缓存列表
        if CacheFeature.game_cache.delay % 10 == 0:
            for bullet in next(self._get_bullets()):
                bullet.reset()
                self.bullets.append(bullet)
        # 消除已失效的子弹，防止内存溢出
        return [bullet for bullet in self.bullets if bullet.alive]

    def level_up(self, enemies):
        """升级"""
        if self.level < 3:
            self.level += 1
            # 播放飞机升级音效
            VolumeFeature.volume_play(self.upgrade_sound)
        else:
            # 当等级为最大值时获得升级补给，则短暂无敌、获得护盾并增加一个炸弹数
            self.invincible = True
            self.shield = True
            self.add_bomb_number(enemies)

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
        self.alive = True
        self.invincible = True
        self.level = 1
        width, height = SettingFeature.screen_setting.screen_size
        self.rect.left, self.rect.bottom = (width - self.rect.width) // 2, height

    def use_bomb(self, enemies):
        """使用炸弹"""
        if self.bomb_number > 0:
            self.bomb_number -= 1
            # 所有敌机扣血100点
            for enemy in enemies:
                enemy: EnemyBase
                if enemy.rect.bottom > 0:
                    enemy.hit_points -= 100

    def _get_bullets(self) -> typing.Generator[typing.List[PlaneBulletBase], None, None]:
        """根据等级获取子弹"""
        if self.level == 1:
            bullets = [PlaneBullet01(self.rect.midtop)]
        elif self.level == 2:
            bullets = [
                PlaneBullet02((self.rect.centerx - 33, self.rect.centery)),
                PlaneBullet02((self.rect.centerx + 33, self.rect.centery))
            ]
        else:
            bullets = [
                PlaneBullet03((self.rect.centerx - 33, self.rect.centery)),
                PlaneBullet03(self.rect.midtop),
                PlaneBullet03((self.rect.centerx + 33, self.rect.centery))
            ]
        while True:
            yield bullets
