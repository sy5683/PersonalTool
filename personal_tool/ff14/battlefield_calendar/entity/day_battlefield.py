import datetime
from typing import Union

from .battlefield_type import BattlefieldType


class DayBattlefield:

    def __init__(self, date: datetime.date):
        self.date = date
        self.battlefield_type: Union[BattlefieldType, None] = None
        self.next_battlefield_type: Union[BattlefieldType, None] = None

    def set_battlefield_type(self, battlefield_type: BattlefieldType):
        self.battlefield_type = battlefield_type

    def set_next_battlefield_type(self, battlefield_type: BattlefieldType):
        self.next_battlefield_type = battlefield_type

    def show(self):
        date_str = self.date.strftime("%Y-%m-%d")
        print(f"==【{date_str}】==")
        print(f"- 今日战场: 【{self.battlefield_type.to_sign()}】")
        print(f"- 23点之后: 【{self.next_battlefield_type.to_sign()}】")
