import random
import typing

import pygame

from .backdrop.airport import Airport
from .bullet.base.bullet_base import BulletBase
from .enemy.base.enemy_base import EnemyBase
from .enemy.enemy_01 import Enemy01
from .enemy.enemy_02 import Enemy02
from .enemy.enemy_03 import Enemy03
from .plane.plane_01 import Plane01
from .supply.bomb_supply import BombSupply
from .supply.med_kit_supply import MedKitSupply
from .supply.star_supply import StarSupply
from ..base.scene_base import SceneBase
from ...volume_feature import VolumeFeature


class GameScene(SceneBase):

    def __init__(self):
        super().__init__("game_scene\\background.png", "game_scene\\bgm.ogg")
        self.level = 0  # 难度等级
        self.score = 0  # 得分
        # 背景
        self.airport = Airport()
        # 飞机
        self.plane = Plane01(5, 3)
        self.bullets = []
        # 敌机
        self.enemies = pygame.sprite.Group()
        # 补给
        self.supplys = [BombSupply(), MedKitSupply(), StarSupply()]
        # 计时器
        self.supply_timer = self.get_timer(5)  # 补给计时器

    def main(self):
        # 播放背景音乐
        pygame.mixer.music.play(-1)

        # 开始动画
        self.airport.reset()

        # 游戏开始前进行一些初始化操作
        # 初始化一些敌机
        self.add_enemy(Enemy01, 5)
        self.add_enemy(Enemy02, 1)
        # 在这里将所有敌机重置，因为运行时的重置会触发得分操作，但是很明显，游戏开始前分数应该是0
        for enemy in self.enemies:
            enemy.reset()

        # 游戏运行
        while self.running:
            # 设置背景音量
            VolumeFeature.set_volume(pygame.mixer.music)

            # 事件检测
            for event in pygame.event.get():
                # 退出游戏
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()  # 终止pygame
                if event.type == pygame.KEYDOWN:
                    # 全屏切换
                    if event.key == pygame.K_F11:
                        # 重新获取窗口对象
                        self.screen = self.get_screen(True)
                # 随机生成补给
                if event.type == self.supply_timer:
                    random.choice(self.supplys).reset()

            # 根据难度设置敌机
            target_scores = [2000, 10000, 30000, 100000, 500000]
            for level, score in enumerate(target_scores):
                if self.level == level and self.score >= score:
                    self.level_up()
                    if level == len(target_scores) - 1:
                        # TODO 出现boss
                        pass

            # 绘制背景
            self.screen.blit(self.image, self.rect)
            self.move()
            # 绘制起飞坪
            if self.airport.alive:
                self.screen.blit(self.airport.image, self.airport.rect)
                self.airport.move()
            # 绘制飞机
            if self.plane.life_number:
                self.screen.blit(self.plane.get_image(), self.plane.rect)
                self.plane.move()
                # 添加子弹到本地缓存列表
                if not self.delay % 10:
                    bullets = next(self.plane.get_bullets())
                    for bullet in bullets:
                        bullet.reset()
                        self.bullets.append(bullet)
                # 消除已失效的子弹，防止数据溢出
                self.bullets: typing.List[BulletBase] = [bullet for bullet in self.bullets if bullet.alive]
            # 绘制敌机
            for enemy in self.enemies:
                enemy: EnemyBase
                if enemy.hit_points > 0:
                    if enemy.hit and enemy.hit_image:
                        self.screen.blit(enemy.hit_image, enemy.rect)
                        enemy.hit = False
                    else:
                        self.screen.blit(enemy.image, enemy.rect)
                    # 绘制血条
                    hit_points_ratio = enemy.hit_points / enemy.max_hit_points
                    if hit_points_ratio < 1:
                        pygame.draw.line(self.screen, (0, 0, 0), (enemy.rect.left, enemy.rect.top - 5),
                                         (enemy.rect.right, enemy.rect.top - 5), 2)
                        # 血量剩余20%显示绿色，否则显示红色
                        hit_points_color = (255, 0, 0) if hit_points_ratio < 0.2 else (0, 255, 0)
                        pygame.draw.line(self.screen, hit_points_color, (enemy.rect.left, enemy.rect.top - 5),
                                         (enemy.rect.left + enemy.rect.width * hit_points_ratio, enemy.rect.top - 5), 2)
                    enemy.move()
                else:
                    # TODO 绘制坠毁动画
                    self.score += enemy.score
                    enemy.reset()
            # 绘制飞机子弹
            for bullet in self.bullets:
                self.screen.blit(bullet.image, bullet.rect)
                bullet.move()
                bullet.attack_enemy(self.enemies)
            # 绘制补给
            for supply in self.supplys:
                if supply.alive:
                    self.screen.blit(supply.image, supply.rect)
                    supply.move()
                    supply.trigger(self.plane, enemies=self.enemies)

            # 游戏结束
            if self.plane.life_number == 0:
                break

            # 更新界面
            pygame.display.flip()
            # 刷新频率
            self.clock.tick(60)
            # 更新延迟
            self.delay = (self.delay + 1) if self.delay < 99 else 0

        # 增加敌机

    def add_enemy(self, enemy, quantity: int):
        for _ in range(quantity):
            self.enemies.add(enemy())

    def level_up(self):
        """难度升级"""
        self.level += 1
        # 增加敌机
        self.add_enemy(Enemy01, 5)
        self.add_enemy(Enemy02, 2)
        self.add_enemy(Enemy03, 1)
        # 提升敌机速度
        for enemy in self.enemies:
            enemy.speed += 1
