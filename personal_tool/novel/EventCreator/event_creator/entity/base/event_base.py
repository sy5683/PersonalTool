from abc import ABCMeta, abstractmethod


class EventBase(metaclass=ABCMeta):
    """事件基类"""

    def __init__(self):
        # 事件基本信息
        self.name = ""
        self.is_done = False
        self.key_roles = []  # 关键角色
        self.partake_size = 9  # 事件参与人数

        # 设置事件信息
        self.set_event_info()
        self.__check_event_info()

    @abstractmethod
    def set_event_info(self):
        """设置事件信息"""

    def __check_event_info(self):
        """校验事件信息"""
        assert self.name, f"事件类【{self.__class__.__name__}】名称未设置"
