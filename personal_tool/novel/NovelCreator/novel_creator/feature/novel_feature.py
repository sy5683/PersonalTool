from cn2an import an2cn

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

    @staticmethod
    def show_outline(novel: Novel):
        """展示小说大纲"""
        print(f"《{novel.novel_name}》")
        print(f"小说梗概:\n{novel.novel_synopsis}\n\n")
        for outline_index, outline in enumerate(novel.outlines):
            print(f"第{an2cn(outline_index + 1)}卷 {outline.outline_name}")
            print(f"大纲梗概:\n{outline.outline_synopsis}\n\n")

    @staticmethod
    def show_content(novel: Novel):
        """展示小说内容"""
        print(f"《{novel.novel_name}》\n")
        print(f"{novel.text}\n\n")
        for outline_index, outline in enumerate(novel.outlines):
            print(f"第{an2cn(outline_index + 1)}卷 {outline.outline_name}\n\n")
            event_index = 0
            for event in outline.events:
                for text_index, text in enumerate(event.text.split("\n\t\n")):
                    event_index += 1
                    print(f"第{an2cn(event_index)}章 {event.title}（{an2cn(text_index + 1)}）")
                    print(f"{text}\n\n")
