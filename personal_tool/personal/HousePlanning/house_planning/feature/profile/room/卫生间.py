import abc

from ..base.room import Room


class CloakRoom(Room, metaclass=abc.ABCMeta):

    def __init__(self, room_name: str):
        super().__init__(room_name)


class MasterCloakRoom(CloakRoom):

    def __init__(self):
        super().__init__("主卫")


class GuestCloakRoom(CloakRoom):

    def __init__(self):
        super().__init__("客卫")
