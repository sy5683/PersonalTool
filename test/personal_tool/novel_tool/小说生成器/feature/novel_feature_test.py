from common_core.base.test_base import TestBase
from common_util.data_util.object_util.object_util import ObjectUtil
from personal_tool.novel_tool.小说生成器.feature.novel_feature import NovelFeature


class NovelFeatureTestCase(TestBase):

    def setUp(self):
        self.novel_name = "构灵"

    def test_get_novel(self):
        novel = NovelFeature.get_novel(self.novel_name)
        ObjectUtil.print_object(novel)

    def test_get_novel_path(self):
        novel_path = NovelFeature._get_novel_path(self.novel_name)
        print(novel_path)
