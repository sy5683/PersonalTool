import pygame

from common_core.base.tool_base import ToolBase
from feature.scene.game_scene.game_scene import GameScene


class AircraftWar(ToolBase):

    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("飞机大战")

    def main(self):
        game_scene = GameScene()
        game_scene.main()


if __name__ == '__main__':
    aircraft_war = AircraftWar()
    aircraft_war.main()
