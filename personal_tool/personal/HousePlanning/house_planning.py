import typing
from enum import Enum

from house_planning.feature.house_plan.base.house_plan import HousePlan
from house_planning.house_plan_001 import HousePlan001


class HousePlanType(Enum):
    house_plan_001 = HousePlan001.get_plan


class HousePlanning:
    """房屋计划"""

    def __init__(self, house_plan: typing.Type[HousePlan]):
        self.house = house_plan.get_plan()

    def main(self):
        self.house.show()


if __name__ == '__main__':
    house_planning = HousePlanning(HousePlan001)
    house_planning.main()
