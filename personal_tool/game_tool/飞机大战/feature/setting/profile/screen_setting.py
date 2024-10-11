import typing


class ScreenSetting:

    def __init__(self):
        self.__full_screen = False
        self.__screen_size = (480, 700)

    @property
    def full_screen(self) -> bool:
        return self.__full_screen

    @full_screen.setter
    def full_screen(self, full_screen: bool):
        self.__full_screen = full_screen

    @property
    def screen_size(self) -> typing.Tuple[int, int]:
        return self.__screen_size

    @screen_size.setter
    def screen_size(self, screen_size: typing.Tuple[int, int]):
        self.__screen_size = screen_size
