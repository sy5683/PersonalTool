from enum import Enum

from common_core.base.tool_base import ToolBase
from feature.novel_feature import NovelFeature


class Operations(Enum):
    show_outline = NovelFeature.show_outline
    show_content = NovelFeature.show_content


class NovelCreator(ToolBase):

    def __init__(self, novel_name: str):
        super().__init__()
        self.novel_name = novel_name

    def main(self, function):
        novel = NovelFeature.get_novel(self.novel_name)
        function(novel)


if __name__ == '__main__':
    novel_creator = NovelCreator("构灵")
    novel_creator.main(Operations.show_outline)
    # novel_creator.main(Operations.show_content)
