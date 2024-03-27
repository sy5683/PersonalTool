import pygame


class KeySetting:

    def __init__(self):
        self.__up_key = pygame.K_w
        self.__down_key = pygame.K_s
        self.__left_key = pygame.K_a
        self.__right_key = pygame.K_d

    @property
    def up_key(self) -> int:
        return self.__up_key

    @up_key.setter
    def up_key(self, up_key: int):
        self.__up_key = up_key

    @property
    def down_key(self) -> int:
        return self.__down_key

    @down_key.setter
    def down_key(self, down_key: int):
        self.__down_key = down_key

    @property
    def left_key(self) -> int:
        return self.__left_key

    @left_key.setter
    def left_key(self, left_key: int):
        self.__left_key = left_key

    @property
    def right_key(self) -> int:
        return self.__right_key

    @right_key.setter
    def right_key(self, right_key: int):
        self.__right_key = right_key
