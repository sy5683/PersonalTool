import abc
import random
import typing
from pathlib import Path

from common_util.code_util.import_util.import_util import ImportUtil
from .outline import Outline


class Novel(metaclass=abc.ABCMeta):
    """小说"""

    def __init__(self, novel_path: Path):
        self.novel_name = novel_path.name  # 小说名称
        self.novel_path = novel_path  # 小说路径
        self.novel_synopsis = self.__get_novel_attribute("novel_synopsis", "小说梗概")
        self.text = self.__get_novel_attribute("text", "正文")
        self.outlines = self._get_outlines()  # 大纲列表

    def _get_outlines(self) -> typing.List[Outline]:
        """获取大纲列表"""
        main_outline_sequence = self.__get_novel_attribute("main_outline_sequence", "主干大纲顺序")
        outlines = []
        outline_paths = list(self.novel_path.joinpath("大纲").glob("*"))
        random.shuffle(outline_paths)
        for outline_path in outline_paths:
            if not outline_path.is_dir():
                continue
            if outline_path.stem == "__pycache__":
                continue
            outline_names = [outline.outline_name for outline in outlines]
            if outline_path.stem in main_outline_sequence or outline_path.stem in outline_names:
                outline_path = outline_path.parent.joinpath(main_outline_sequence.pop(0))
            outlines.append(Outline(outline_path))
        return outlines

    def __get_novel_attribute(self, attribute_key: str, attribute_name: str = ''):
        """获取小说参数"""
        # 相对导入目标小说文件夹，获取其下__init__.py中的各种参数
        novel_module = ImportUtil.import_module(self.novel_path)
        try:
            attribute_value = getattr(novel_module, attribute_key)
            attribute_value = attribute_value.strip("\n") if isinstance(attribute_value, str) else attribute_value
            return attribute_value
        except AttributeError:
            raise AttributeError(f"小说【{self.novel_name}】中缺少{attribute_name}: {attribute_key}")
