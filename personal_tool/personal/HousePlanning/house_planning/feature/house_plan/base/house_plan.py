import abc

from ...profile.base.house import House


class HousePlan(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def get_plan() -> House:
        """"""
