class GameCache:

    def __init__(self):
        self.__delay = 0

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, delay):
        self.__delay = 0 if delay == 100 else delay
