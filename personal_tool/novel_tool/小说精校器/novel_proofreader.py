from enum import Enum

from common_core.base.tool_base import ToolBase
from common_util.file_util.file_util.file_util import FileUtil
from feature.title_feature import TitleFeature


class Operations(Enum):
    craw_titles = TitleFeature.craw_titles
    replace_titles = TitleFeature.replace_titles


class NovelProofreader(ToolBase):

    def main(self, function, **kwargs):
        function(**kwargs)


if __name__ == '__main__':
    novel_proofreader = NovelProofreader()
    # novel_proofreader.main(Operations.craw_titles)
    novel_proofreader.main(Operations.replace_titles, novel_path=FileUtil.get_file_path())
