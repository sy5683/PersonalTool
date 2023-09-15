from abc import ABCMeta
from typing import Union


class Furniture(metaclass=ABCMeta):

    def __init__(self, furniture_name: str, price: Union[int, float]):
        self.furniture_name = furniture_name  # 家具名称
        self.price = float(price)  # 价格
        self.is_bought = False  # 是否已购买

    def bought(self):
        """家具已买"""
        self.is_bought = True
        return self

    def show(self):
        print(f"{self.furniture_name}: {self.price}")
