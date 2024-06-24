import random
import typing

import pygame

from .base.enemy_base import EnemyBase
from .bullet.base.boss_bullet_base import BossBulletBase
from .bullet.boss_bullet_01 import BossBullet01
from .bullet.boss_bullet_02 import BossBullet02
from .bullet.boss_bullet_03 import BossBullet03
from .bullet.boss_bullet_04 import BossBullet04
from ....file_feature import FileFeature


class Boss(EnemyBase):

    def __init__(self):
        image_names = ["game_scene\\enemy\\boss.png",
                       "game_scene\\enemy\\boss_2.png",
                       "game_scene\\enemy\\boss_3.png",
                       "game_scene\\enemy\\boss_4.png"]
        super().__init__(image_names, 10000, 1, 1000000)
        # 设置Boss参数
        self.bullets: typing.List[BossBulletBase] = []
        self.rect.left, self.rect.top = 0, -250

    def draw(self, screen: pygame.Surface):
        """绘制Boss"""
        # TODO hit图片需要做到叠加，而不是替换
        hit_image = FileFeature.load_image("game_scene\\enemy\\boss_hit.png")
        screen.blit(hit_image if self.hit else self.get_image(), self.rect)
        self.draw_hit_points_ratio(screen, 10, 5)
        self.hit = False

    def get_bullets(self) -> typing.List[BossBulletBase]:
        """获取子弹"""
        # 消除已失效的子弹，防止内存溢出
        return [bullet for bullet in self.bullets if bullet.alive]

    def move(self):
        """Boss移动"""
        self.rect.top += self.speed if self.rect.top < 0 else 0

    def reset_bullets(self):
        """重置Boss攻击"""
        # 使当前的子弹失效
        for bullet in self.bullets:
            bullet.alive = False
        # 添加子弹到缓存列表
        for bullet in next(self._get_bullets()):
            bullet.reset()
            self.bullets.append(bullet)

    def _get_bullets(self) -> typing.Generator[typing.List[BossBulletBase], None, None]:
        """随机获取子弹"""
        # 攻击方式一
        bullets_01 = []
        vital_number = random.randint(0, 8)
        for index, col in enumerate(range(0, 480, 40)):
            if index in range(vital_number, vital_number + 4):
                continue
            bullets_01.append(BossBullet01((col, 0)))
        # 攻击方式二
        bullets_02 = [BossBullet02((0, 5)),
                      BossBullet02((-2, 4)), BossBullet02((2, 4)),
                      BossBullet02((-4, 3)), BossBullet02((4, 3))]
        # 攻击方式三
        bullets_03 = [BossBullet03((135, self.rect.bottom)), BossBullet03((310, self.rect.bottom))]
        # 攻击方式四
        bullets_04 = [BossBullet04() for _ in range(random.randint(2, 5))]
        bullets = random.choice([bullets_01, bullets_02, bullets_03, bullets_04])
        while True:
            yield bullets
