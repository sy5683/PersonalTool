from abc import ABCMeta, abstractmethod

from ...profile.base.house import House


class HousePlan(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def get_plan() -> House:
        """"""
