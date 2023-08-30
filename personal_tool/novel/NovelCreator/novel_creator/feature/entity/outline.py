import sys
from pathlib import Path
from typing import List

from .event import Event


class Outline:
    """大纲"""

    def __init__(self, outline_path: Path):
        self.__outline_path = outline_path  # 大纲路径
        self.outline_name = outline_path.stem  # 大纲名称
        self.synopsis = """"""  # 大纲梗概
        self.events = self._get_events()  # 事件列表

    def _get_events(self) -> List[Event]:
        """获取事件列表"""
        events = []
        for event_class in Event.__subclasses__():
            event = event_class()
            event_path = Path(sys.modules[event.__module__].__file__)
            if event_path.parent == self.__outline_path:
                events.append(event)
        return events
