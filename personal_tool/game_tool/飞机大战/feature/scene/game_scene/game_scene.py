import random
import sys

import pygame
from pygame import USEREVENT

from .backdrop.airport import Airport
from .plane.plane_01 import Plane01
from .supply.bomb_supply import BombSupply
from .supply.med_kit_supply import MedKitSupply
from .supply.star_supply import StarSupply
from ..base.scene_base import SceneBase


class GameScene(SceneBase):

    def __init__(self):
        super().__init__("images\\game_scene\\background.png")
        # 背景
        self.airport = Airport()
        self.clouds = []
        # 飞机
        self.plane = Plane01(5, 3)
        # 补给
        self.supplys = [BombSupply(), MedKitSupply(), StarSupply()]

    def main(self):
        supply_time = USEREVENT + 2  # 补给计时器
        pygame.time.set_timer(supply_time, 7 * 1000)

        self.airport.reset()

        while True:

            # 事件检测
            for event in pygame.event.get():
                # 退出游戏
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # 全屏切换
                    if event.key == pygame.K_F11:
                        # 重新获取窗口对象
                        self.screen = self.get_screen(True)

                # 随机生成补给
                if event.type == supply_time:
                    random.choice(self.supplys).reset()

            # 绘制背景
            self.screen.blit(self.image, (0, 0))
            # 绘制起飞坪
            if self.airport.active:
                self.screen.blit(self.airport.image, self.airport.rect)
                self.airport.move()
            # 绘制飞机
            if self.plane.life_number:
                self.screen.blit(self.plane.get_image(), self.plane.rect)
                self.plane.move()  # 控制飞机移动
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
