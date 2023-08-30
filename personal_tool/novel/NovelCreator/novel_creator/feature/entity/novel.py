from typing import List

from .outline import Outline
from ...feature.path_feature import PathFeature


class Novel:
    """小说"""

    def __init__(self, novel_name: str):
        self.novel_name = novel_name  # 小说名称
        self.__novel_path = PathFeature.to_novel_path(self.novel_name)  # 小说路径
        self.outlines = self._get_outlines()  # 大纲列表

    def _get_outlines(self) -> List[Outline]:
        """获取大纲列表"""
        outline_paths = [outline_path for outline_path in self.__novel_path.glob("*") if outline_path.is_dir()]
        return [Outline(outline_path) for outline_path in outline_paths]
