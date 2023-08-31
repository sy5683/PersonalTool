import sys
from abc import ABCMeta, abstractmethod
from pathlib import Path


class Event(metaclass=ABCMeta):
    """事件"""

    def __init__(self):
        __event_path = Path(sys.modules[self.__module__].__file__)
        self.event_name = __event_path.stem  # 事件名称
        self.is_done = False  # 是否完成
        self.key_roles = []  # 关键角色
        self.partake_size = 9  # 事件参与人数

        self.set_event_info()
        self.__check_event_info()

    @abstractmethod
    def set_event_info(self):
        """设置事件信息"""

    def __check_event_info(self):
        """校验事件信息"""
