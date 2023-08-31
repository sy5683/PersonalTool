import sys
from abc import ABCMeta
from pathlib import Path
from typing import List

from .event import Event
from ...util.import_util import ImportUtil


class Outline(metaclass=ABCMeta):
    """大纲"""

    def __init__(self, outline_path: Path):
        self.__outline_path = outline_path  # 大纲路径
        self.outline_name = outline_path.stem  # 大纲名称
        self.outline_synopsis = self._get_outline_synopsis()  # 大纲梗概
        self.events = self._get_events()  # 事件列表

    def _get_outline_synopsis(self) -> str:
        """获取大纲梗概"""
        # 相对导入目标大纲文件夹，获取其下__init__.py中的大纲梗概
        module = ImportUtil.import_module(self.__outline_path)
        try:
            return module.outline_synopsis
        except AttributeError:
            raise Exception(f"大纲【{self.outline_name}】中缺少大纲梗概")

    def _get_events(self) -> List[Event]:
        """获取事件列表"""
        events = []
        for event_class in Event.__subclasses__():
            event = event_class()
            if str(self.__outline_path) in str(Path(sys.modules[event.__module__].__file__)):
                events.append(event)
        return events
