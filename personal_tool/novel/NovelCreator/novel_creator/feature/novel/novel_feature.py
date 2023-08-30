from typing import List

from personal_tool.novel.NovelCreator.novel_creator.feature.novel.entity.event import Event
from personal_tool.novel.NovelCreator.novel_creator.feature.novel.entity.novel import Novel
from personal_tool.novel.NovelCreator.novel_creator.feature.path_feature import PathFeature
from personal_tool.novel.NovelCreator.novel_creator.util.import_util import ImportUtil


# class GouLingOutline(Enum):
#     wishing_ball = {
#         'outline_name': "许愿龙珠",
#         'synopsis': """
#         """,
#     }
#     university_world_cup = {
#         'outline_name': "学院世界杯",
#         'synopsis': """
#         """,
#     }
#     system_owner_war = {
#         'outline_name': "系统者纷争",
#         'synopsis': """
#         """,
#     }
#
#
# class NovelType(Enum):
#     gou_ling = {
#         'novel_name': "构灵",
#         'outline': GouLingOutline
#     }
#

class NovelFeature:
    _novel = None

    @classmethod
    def get_novel(cls, novel_name: str) -> Novel:
        """获取小说对象"""
        if cls._novel is None:
            # 1) 首先获取所有事件对象（最底层对象）
            ImportUtil.import_module(PathFeature.to_novel_path())  # 使用subclasses之前必须将子类导入
            cls._novel = Novel(novel_name)
        return cls._novel
