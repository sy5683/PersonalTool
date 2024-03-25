class ScreenConfig:

    def __init__(self):
        self.__full_screen = False

    @property
    def full_screen(self) -> bool:
        return self.__full_screen

    @full_screen.setter
    def full_screen(self, full_screen: bool):
        self.__full_screen = full_screen
