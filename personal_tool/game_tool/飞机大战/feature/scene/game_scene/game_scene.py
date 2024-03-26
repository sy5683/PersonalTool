import sys

import pygame

from .plane.player1_plane import Player1Plane
from ..base.scene_base import SceneBase


class GameScene(SceneBase):

    def __init__(self):
        super().__init__("images\\game_scene\\background.png")
        self.player1_plane = Player1Plane((self.width, self.height))

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

            # 操作
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
                self.player1_plane.move_up()
            if key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
                self.player1_plane.move_down()
            if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
                self.player1_plane.move_left()
            if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
                self.player1_plane.move_right()

            # 绘制背景
            self.screen.blit(self.image, (0, 0))
            # 绘制飞机
            self.screen.blit(self.player1_plane.image, self.player1_plane.rect)

            # 更新界面
            pygame.display.flip()
            # 刷新频率
            self.clock.tick(60)
