class GameCache:

    def __init__(self):
        self.__angle = 0
        self.__delay = 0

    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, angle):
        self.__angle = 0 if angle == 360 else angle

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, delay):
        self.__delay = 0 if delay == 100 else delay
