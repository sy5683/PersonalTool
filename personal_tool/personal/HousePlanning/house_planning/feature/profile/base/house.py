import typing

from .room import Room
from ....util.float_util import FloatUtil


class House:

    def __init__(self):
        # self.area = None  # 面积
        # self.construction_ratio = None  # 得房率
        self.rooms: typing.List[Room] = []  # 房间
        self.all_furniture_price = 0.0  # 家具合计金额

    def add_room(self, room: Room):
        self.rooms.append(room)
        self.all_furniture_price = FloatUtil.add(self.all_furniture_price, room.all_furniture_price)

    def show(self):
        print("房子")
        for room in self.rooms:
            room.show()
        print(f"合计金额: {self.all_furniture_price}")
