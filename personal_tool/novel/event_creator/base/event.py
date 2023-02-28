from abc import ABCMeta, abstractmethod


class Event(metaclass=ABCMeta):
    """事件"""

    def __init__(self):
        # 事件基本信息
        self.place = None

        # 设置事件信息
        self.set_event_info()
        self.__check_event_inifo()

    @abstractmethod
    def set_event_info(self):
        """设置事件信息"""

    def __check_event_inifo(self):
        """校验事件信息"""
        assert self.place is not None, f"事件【{self.__class__.__name__}】地点未设置"
