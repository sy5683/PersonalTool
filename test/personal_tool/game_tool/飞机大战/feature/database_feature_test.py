from common_core.base.test_base import TestBase
from common_util.data_util.object_util.object_util import ObjectUtil
from personal_tool.game_tool.飞机大战.feature.database.database_feature import DatabaseFeature


class DatabaseFeatureTestCase(TestBase):

    def setUp(self):
        self.table_name = "Score"

    def test_get_scores(self):
        scores = DatabaseFeature.get_scores()
        self.assertNotEqual(scores, None)
        ObjectUtil.print_object(scores)

    def test_save_score(self):
        self.assertEqual(DatabaseFeature.save_score("admin", 5000), None)
