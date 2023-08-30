from enum import Enum

from novel_creator.feature.novel_feature import NovelFeature


class Operations(Enum):
    show_outline = NovelFeature.show_outline


class NovelCreator:
    """小说生成器"""

    def main(self, novel_name: str, function=None):
        novel = NovelFeature.get_novel(novel_name)
        if function:
            function(novel)


if __name__ == '__main__':
    novel_creator = NovelCreator()
    novel_creator.main("构灵", Operations.show_outline)
