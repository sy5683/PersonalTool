import random

import pygame

from .backdrop.airport import Airport
from .enemy.base.enemy_base import EnemyBase
from .enemy.boss import Boss
from .enemy.enemy_01 import Enemy01
from .enemy.enemy_02 import Enemy02
from .enemy.enemy_03 import Enemy03
from .plane.plane_01 import Plane01
from .supply.bomb_supply import BombSupply
from .supply.med_kit_supply import MedKitSupply
from .supply.star_supply import StarSupply
from ..base.scene_base import SceneBase
from ...cache.cache_feature import CacheFeature
from ...file_feature import FileFeature
from ...volume_feature import VolumeFeature


class GameScene(SceneBase):

    def __init__(self):
        super().__init__("game_scene\\background.png", "game_scene\\bgm.ogg")
        self.level = 0  # 难度等级
        self.score = 0  # 得分
        self.paused = False  # 暂停
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
        self.invincible_timer = self.get_timer(3)  # 无敌计时器

    def main(self):
        # 播放背景音乐
        pygame.mixer.music.play(-1)

        # 游戏开始前进行一些初始化操作
        # 开始动画
        self.airport.reset()
        # 初始化飞机
        self.plane.reset()
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
                        # 切换屏幕暂停游戏
                        self.paused = True
                # 计时器
                if event.type == self.supply_timer:
                    random.choice(self.supplys).reset()  # 随机生成补给
                if event.type == self.invincible_timer:
                    self.plane.invincible = False  # 结束飞机无敌

            # 根据难度设置敌机
            # target_scores = [2000, 10000, 30000, 100000, 500000]
            target_scores = [100]  # TODO
            for level, score in enumerate(target_scores):
                if self.level == level and self.score >= score:
                    self.level_up()
                    if level == len(target_scores) - 1:
                        self.add_enemy(Boss)
                        pass

            # 绘制背景
            self.screen.blit(self.image, self.rect)
            self.move()
            # 绘制起飞坪
            if self.airport.alive:
                self.airport.draw(self.screen)
                self.airport.move()
            # 绘制飞机
            if self.plane.alive:
                self.plane.draw(self.screen)
                self.plane.move()
            else:
                self.plane.draw_crash(self.screen)
                self.plane.reset()
            # 绘制敌机
            for enemy in self.enemies:
                enemy: EnemyBase
                if enemy.hit_points > 0:
                    enemy.draw(self.screen)
                    enemy.move()
                else:
                    enemy.draw_crash(self.screen)
                    self.score += enemy.score
                    enemy.reset()
            # 绘制飞机子弹
            for bullet in self.plane.get_bullets():
                bullet.draw(self.screen)
                bullet.move()
                bullet.attack_enemy(self.enemies)
            # 绘制补给
            for supply in self.supplys:
                if supply.alive:
                    supply.draw(self.screen)
                    supply.move()
                    supply.trigger(self.plane, enemies=self.enemies)
            # 显示得分
            self.score_font.render(f"Score: {self.score}")

            # 游戏结束
            if self.plane.life_number == 0:
                break

            # 更新界面
            pygame.display.flip()
            # 刷新频率
            self.clock.tick(60)
            # 更新延迟
            CacheFeature.game_cache.delay += 1

    def add_enemy(self, enemy, quantity: int = 1):
        """增加敌机"""
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
