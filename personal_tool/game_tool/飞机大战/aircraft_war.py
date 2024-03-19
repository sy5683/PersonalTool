import pygame

from common_core.base.tool_base import ToolBase
from personal_tool.game_tool.飞机大战.feature.scene.game_scene.game_scene import GameScene


class AircraftWar(ToolBase):

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

    def main(self):
        game_scene = GameScene()
        game_scene.main()


if __name__ == '__main__':
    aircraft_war = AircraftWar()
    aircraft_war.main()
