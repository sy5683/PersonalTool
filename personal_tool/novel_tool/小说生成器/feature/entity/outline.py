import abc
import typing
from pathlib import Path

from common_util.code_util.import_util.import_util import ImportUtil
from .event import Event


class Outline(metaclass=abc.ABCMeta):
    """大纲"""

    def __init__(self, outline_path: Path):
        self.__outline_path = outline_path  # 大纲路径
        self.outline_name = outline_path.stem  # 大纲名称
        self.outline_synopsis = self.__get_outline_attribute("outline_synopsis", "大纲梗概")
        self.events = self._get_events()  # 事件列表

    def _get_events(self) -> typing.List[Event]:
        """获取事件列表"""
        events = []
        for event_class in Event.__subclasses__():
            event = event_class()
            if str(self.__outline_path) in str(event.event_path):
                events.append(event)
        return events

    def __get_outline_attribute(self, attribute_key: str, attribute_name: str = ''):
        """获取大纲参数"""
        # 相对导入目标大纲文件夹，获取其下__init__.py中的大纲梗概
        outline_module = ImportUtil.import_module(self.__outline_path)
        try:
            attribute_value = getattr(outline_module, attribute_key)
            attribute_value = attribute_value.strip("\n") if isinstance(attribute_value, str) else attribute_value
            return attribute_value
        except AttributeError:
            raise AttributeError(f"大纲【{self.outline_name}】中缺少{attribute_name}: {attribute_key}")
