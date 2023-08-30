from abc import ABCMeta, abstractmethod


class Event(metaclass=ABCMeta):
    """事件"""

    def __init__(self, event_name: str = ''):
        self.event_name = event_name  # 事件名称

        self.set_event_info()
        self.__check_event_info()

    # @abstractmethod
    def set_event_info(self):
        """设置事件信息"""

    def __check_event_info(self):
        """校验事件信息"""
        assert self.event_name, f"事件类【{self.__class__.__name__}】名称未设置"


