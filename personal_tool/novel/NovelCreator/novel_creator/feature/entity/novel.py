import importlib
from abc import ABCMeta
from typing import List

from .outline import Outline
from ...feature.path_feature import PathFeature


class Novel(metaclass=ABCMeta):
    """小说"""

    def __init__(self, novel_name: str):
        self.novel_name = novel_name  # 小说名称
        self.__novel_path = PathFeature.to_novel_path(self.novel_name)  # 小说路径
        self.novel_synopsis = self._get_novel_synopsis()  # 小说梗概
        self.outlines = self._get_outlines()  # 大纲列表

    def _get_novel_synopsis(self) -> str:
        """获取小说梗概"""
        # 相对导入目标小说文件夹，获取其下__init__.py中的小说梗概
        params = importlib.import_module(f"novel_creator.小说.{self.novel_name}")
        try:
            return params.novel_synopsis
        except AttributeError:
            raise Exception(f"小说【{self.novel_name}】中缺少小说梗概")

    def _get_outlines(self) -> List[Outline]:
        """获取大纲列表"""
        outlines = []
        for outline_path in self.__novel_path.joinpath("大纲").glob("*"):
            if not outline_path.is_dir():
                continue
            if outline_path.stem == "__pycache__":
                continue
            outlines.append(Outline(outline_path))
        return outlines
