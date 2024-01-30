from common_core.base.test_base import TestBase
from common_util.code_util.database_util.database_util import DatabaseUtil


class DatabaseUtilTestCase(TestBase):

    def setUp(self) -> None:
        self.sqlite_path = self.get_test_file("测试.sqlite")

    def test_get_database_connect(self):
        database_connect = DatabaseUtil.get_database_connect(sqlite_path=self.sqlite_path)
        self.assertNotEqual(database_connect, None)
        print(database_connect)

        table_name = "Test"
        database_connect.execute_sql(f"SELECT name FROM pragma_table_info('{table_name}');")
        print(database_connect.get_results())
