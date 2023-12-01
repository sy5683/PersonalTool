from pathlib import Path

import cn2an

from common_util.code_util.import_util.import_util import ImportUtil
from .entity.novel import Novel


class NovelFeature:
    _novel = None

    @classmethod
    def get_novel(cls, novel_name: str) -> Novel:
        """获取小说对象"""
        if cls._novel is None:
            # 取数之前需要将子类导入
            novel_path = cls._get_novel_path(novel_name)
            ImportUtil.import_modules(novel_path)
            cls._novel = Novel(novel_path)
        return cls._novel

    @staticmethod
    def show_outline(novel: Novel):
        """展示小说大纲"""
        print(f"《{novel.novel_name}》")
        print(f"小说梗概:\n{novel.novel_synopsis}\n\n")
        for outline_index, outline in enumerate(novel.outlines):
            print(f"第{cn2an.an2cn(outline_index + 1)}卷 {outline.outline_name}")
            print(f"大纲梗概:\n{outline.outline_synopsis}\n\n")

    @staticmethod
    def show_content(novel: Novel):
        """展示小说内容"""
        print(f"《{novel.novel_name}》\n")
        print(f"{novel.text}\n\n")
        for outline_index, outline in enumerate(novel.outlines):
            print(f"第{cn2an.an2cn(outline_index + 1)}卷 {outline.outline_name}\n\n")
            event_index = 0
            for event in outline.events:
                for text_index, text in enumerate(event.text.split("\n\t\n")):
                    event_index += 1
                    print(f"第{cn2an.an2cn(event_index)}章 {event.title}（{cn2an.an2cn(text_index + 1)}）")
                    print(f"{text}\n\n")

    @staticmethod
    def _get_novel_path(novel_name: str) -> Path:
        """获取小说路径"""
        novel_path = Path(__file__).parent.joinpath(f"profile\\{novel_name}")
        assert novel_path.is_dir(), f"小说不存在: {novel_name}"
        return novel_path
