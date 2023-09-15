from typing import Union

from ..base.furniture import Furniture


class AirCondition(Furniture):

    def __init__(self, price: Union[int, float]):
        super().__init__("空调", price)


class HangingAirCondition(AirCondition):

    def __init__(self, price: Union[int, float]):
        super().__init__(price)
        self.furniture_name = "挂式空调"
