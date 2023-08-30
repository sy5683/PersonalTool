from typing import List

from personal_tool.novel.NovelCreator.novel_creator.feature.novel.entity.event import Event


class Outline:
    """大纲"""

    def __init__(self, outline_name: str):
        self.outline_name = outline_name  # 大纲名称
        self.synopsis = """"""  # 大纲梗概
        self.events: List[Event] = []  # 事件列表
