import unittest

from personal_tool.game.GameCode.game_code.feature.sql_feature.sql_feature import SqlFeature


class SqlFeatureTestCase(unittest.TestCase):

    def test_find_item(self):
        result = SqlFeature.find_item("测试")
        self.assertNotEqual(result, False)
        print(result)

    def test_find_items(self):
        results = SqlFeature.find_items()
        self.assertNotEqual(results, None)
        for result in results:
            print(result)

    def test_add_usage_count(self):
        self.assertEqual(SqlFeature.add_usage_count("测试"), None)

    def test_add_item(self):
        self.assertEqual(SqlFeature.add_item("测试", "test_123"), None)

    def tearDown(self) -> None:
        SqlFeature.connect_close()
