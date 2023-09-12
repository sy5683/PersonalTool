from .entity.novel import Novel
from ..feature.path_feature import PathFeature
from ..util.import_util import ImportUtil


class NovelFeature:
    _novel = None

    @classmethod
    def get_novel(cls, novel_name: str) -> Novel:
        """获取小说对象"""
        if cls._novel is None:
            # 1) 首先获取所有事件对象（最底层对象）
            ImportUtil.import_modules(PathFeature.to_novel_path())  # 使用subclasses之前必须将子类导入
            cls._novel = Novel(novel_name)
        return cls._novel
