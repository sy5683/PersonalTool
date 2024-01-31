from common_core.base.test_base import TestBase
from common_util.code_util.database_util.database_util import DatabaseUtil
from common_util.data_util.object_util.object_util import ObjectUtil


class DatabaseUtilTestCase(TestBase):

    def setUp(self) -> None:
        self.sqlite_path = self.get_test_file("测试.sqlite")
        self.database_connect = DatabaseUtil.get_database_connect(sqlite_path=self.sqlite_path)
        self.table_name = "Test"

    def test_get_data_list(self):
        data_list = DatabaseUtil.get_data_list(self.database_connect, self.table_name)
        ObjectUtil.print_object(data_list)
