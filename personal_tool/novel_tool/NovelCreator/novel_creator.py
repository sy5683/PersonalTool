from enum import Enum

from novel_creator.feature.novel_feature import NovelFeature
from novel_creator.show_novel import ShowNovel


class Operations(Enum):
    show_outline = ShowNovel.show_outline
    show_content = ShowNovel.show_content


class NovelCreator:
    """小说生成器"""

    def __init__(self, novel_name: str):
        self.novel_name = novel_name

    def main(self, function):
        novel = NovelFeature.get_novel(self.novel_name)
        function(novel)


if __name__ == '__main__':
    novel_creator = NovelCreator("构灵")
    novel_creator.main(Operations.show_outline)
    # novel_creator.main(Operations.show_content)
