import sys

import pygame

from .plane.plane_01 import Plane01
from ..base.scene_base import SceneBase


class GameScene(SceneBase):

    def __init__(self):
        super().__init__("images\\game_scene\\background.png")
        self.plane = Plane01((self.width, self.height))

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

            # 绘制背景
            self.screen.blit(self.image, (0, 0))
            # 绘制飞机
            self.screen.blit(self.plane.image, self.plane.rect)
            self.plane.move()  # 控制飞机移动

            # 更新界面
            pygame.display.flip()
            # 刷新频率
            self.clock.tick(60)
