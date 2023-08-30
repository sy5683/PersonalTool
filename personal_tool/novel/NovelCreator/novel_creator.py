from personal_tool.novel.NovelCreator.novel_creator.feature.novel.novel_feature import NovelFeature


class NovelCreator:
    """小说生成器"""

    def main(self, novel_name: str):
        novel = NovelFeature.get_novel(novel_name)
        novel.show_outline()


if __name__ == '__main__':
    novel_creator = NovelCreator()
    novel_creator.main("构灵")
