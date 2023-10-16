import abc

from ..base.room import Room


class Bedroom(Room, metaclass=abc.ABCMeta):

    def __init__(self, room_name: str):
        super().__init__(room_name)


class MasterBedroom(Bedroom):

    def __init__(self):
        super().__init__("主卧")


class SecondBedroom(Bedroom):

    def __init__(self):
        super().__init__("次卧")
