import random
from pathlib import Path
from typing import List

from .base.event_base import EventBase
from ...util.import_util import ImportUtil


class EventFeature:
    ImportUtil.import_module(Path(__file__).parent.joinpath("entity"))
    _all_events: List[EventBase] = None

    #
    @classmethod
    def get_all_events(cls):
        """获取所有事件"""
        if cls._all_events is None:
            cls._all_events = [event() for event in EventBase.__subclasses__()]
        return cls._all_events

    @classmethod
    def get_undone_event(cls) -> EventBase:
        """获取随机未发生事件"""
        all_events = cls.get_all_events()
        undone_events = [event for event in all_events if not event.is_done]
        if undone_events:
            return random.choice(undone_events)
