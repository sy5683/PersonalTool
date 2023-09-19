from abc import ABCMeta
from typing import List

from .furniture import Furniture
from ....util.float_util import FloatUtil


class Room(metaclass=ABCMeta):

    def __init__(self, room_name: str):
        self.room_name = room_name  # 房间名称
        self.furniture: List[Furniture] = []  # 家具
        self.all_furniture_price = 0.0  # 家具合计金额

    def add_furniture(self, furniture: Furniture):
        self.furniture.append(furniture)
        self.all_furniture_price = FloatUtil.add_float(self.all_furniture_price, furniture.price)

    def show(self):
        print(f"【{self.room_name}】 合计: {self.all_furniture_price}")
        for furniture in self.furniture:
            furniture.show()