import sys

import pygame

from ..base.scene_base import SceneBase


class GameScene(SceneBase):

    def __init__(self):
        super().__init__("images\\game_scene\\background.png")

    def main(self):
        # 绘制背景
        self.screen.blit(self.background_image, (0, 0))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # 更新界面
            pygame.display.flip()
            # 刷新频率
            self.clock.tick(60)
