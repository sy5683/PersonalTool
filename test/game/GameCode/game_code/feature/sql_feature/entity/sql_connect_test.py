import unittest

from personal_tool.game.GameCode.game_code.feature.sql_feature.entity.sql_connect import SqlConnect


class SqlConnectTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.sql_connect = SqlConnect()
        self.table_name = "fallout4_code"

    def test_select(self):
        results = self.sql_connect.select(f"SELECT * FROM {self.table_name};")
        for result in results:
            print(result)

    def tearDown(self) -> None:
        self.sql_connect.close()
