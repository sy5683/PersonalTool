import sys

import pygame

from .plane.plane_01 import Plane01
from .supply.bomb_supply import BombSupply
from .supply.med_kit_supply import MedKitSupply
from .supply.star_supply import StarSupply
from ..base.scene_base import SceneBase


class GameScene(SceneBase):

    def __init__(self):
        super().__init__("images\\game_scene\\background.png")
        # 飞机
        self.plane = Plane01(5, 3)
        # 补给
        self.bomb_supply = BombSupply()
        self.med_kit_supply = MedKitSupply()
        self.star_supply = StarSupply()

    def main(self):

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

                # # 随机生成补给
                # if event.type == supply_time:
                #     random.choice([self.bomb_supply, self.med_kit_supply, self.star_supply]).reset()
            if not self.bomb_supply.active:
                self.bomb_supply.reset()

            # 绘制背景
            self.screen.blit(self.image, (0, 0))
            # 绘制飞机
            if self.plane.life_number:
                self.screen.blit(self.plane.get_image(), self.plane.rect)
                self.plane.move()  # 控制飞机移动
            # 绘制补给
            if self.bomb_supply.active:
                self.screen.blit(self.bomb_supply.image, self.bomb_supply.rect)
                self.bomb_supply.move()
                self.bomb_supply.trigger(self.plane)
            if self.med_kit_supply.active:
                self.screen.blit(self.med_kit_supply.image, self.med_kit_supply.rect)
                self.med_kit_supply.move()
                self.med_kit_supply.trigger(self.plane)
            if self.star_supply.active:
                self.screen.blit(self.star_supply.image, self.star_supply.rect)
                self.star_supply.move()
                self.star_supply.trigger(self.plane)

            # 游戏结束
            if self.plane.life_number == 0:
                break

            # 更新界面
            pygame.display.flip()
            # 刷新频率
            self.clock.tick(60)
