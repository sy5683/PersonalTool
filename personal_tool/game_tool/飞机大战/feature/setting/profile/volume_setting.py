class VolumeSetting:

    def __init__(self):
        self.__main_volume = 100

    @property
    def main_volume(self) -> int:
        return self.__main_volume

    @main_volume.setter
    def main_volume(self, volume: int):
        self.__main_volume = min(max(0, volume), 100)
