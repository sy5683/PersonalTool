from typing import List

from personal_tool.novel.NovelCreator.novel_creator.feature.novel.entity.outline import Outline
from personal_tool.novel.NovelCreator.novel_creator.feature.path_feature import PathFeature


class Novel:
    """小说"""

    def __init__(self, novel_name: str):
        self.novel_name = novel_name  # 小说名称
        self.__novel_path = PathFeature.to_novel_path(self.novel_name)
        self.outlines = self._get_outlines()  # 大纲列表

    def show_outline(self):
        """展示小说大纲"""
        print(f"《{self.novel_name}》\n")
        for index, outline in enumerate(self.outlines):
            print(f"第{index + 1}章 {outline.outline_name}")

    def _get_outlines(self) -> List[Outline]:
        """获取大纲"""
        outline_names = [each.stem for each in self.__novel_path.glob("*") if each.is_dir()]
        return [Outline(outline_name) for outline_name in outline_names]
