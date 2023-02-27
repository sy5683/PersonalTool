from abc import ABCMeta


class Event(metaclass=ABCMeta):
    """事件"""

    def __init__(self):
        self.place = None
