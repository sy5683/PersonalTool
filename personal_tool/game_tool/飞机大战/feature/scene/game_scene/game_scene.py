import random

import pygame

from .backdrop.airport import Airport
from .plane.plane_01 import Plane01
from .supply.bomb_supply import BombSupply
from .supply.med_kit_supply import MedKitSupply
from .supply.star_supply import StarSupply
from ..base.scene_base import SceneBase
from ...volume_feature import VolumeFeature


class GameScene(SceneBase):

    def __init__(self):
        super().__init__("game_scene\\background.png", "game_scene\\bgm.ogg")
        # 背景
        self.airport = Airport()
        self.clouds = []
        # 飞机
        self.plane = Plane01(5, 3)
        self.bullets = []
        # 敌机
        self.enemies = []
        # 补给
        self.supplys = [BombSupply(), MedKitSupply(), StarSupply()]
        # 计时器
        self.supply_timer = self.get_timer(5)  # 补给计时器

    def main(self):
        # 播放背景音乐
        pygame.mixer.music.play(-1)

        # 开始动画
        self.airport.reset()

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

            # 绘制背景
            self.screen.blit(self.image, self.rect)
            self.move()
            # 绘制起飞坪
            if self.airport.active:
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
                self.bullets = [bullet for bullet in self.bullets if bullet.active]
                # 绘制飞机子弹
                for bullet in self.bullets:
                    self.screen.blit(bullet.image, bullet.rect)
                    bullet.move()
            # 绘制补给
            for supply in self.supplys:
                if supply.active:
                    self.screen.blit(supply.image, supply.rect)
                    supply.move()
                    supply.trigger(self.plane)

            # 游戏结束
            if self.plane.life_number == 0:
                break

            # 更新界面
            pygame.display.flip()
            # 刷新频率
            self.clock.tick(60)
            # 更新延迟
            self.delay = (self.delay + 1) if self.delay < 99 else 0