from common_core.base.test_base import TestBase
from common_util.data_util.object_util.object_util import ObjectUtil
from common_util.system_util.database_util.database_util import DatabaseUtil


class DatabaseUtilTestCase(TestBase):

    def test_get_mysql_connect(self):
        database_connect = DatabaseUtil.get_database_connect(ip='localhost', port=5683, database_name='Test',
                                                             username='root', password='ggdd947')
        self.assertNotEqual(database_connect, None)
        table_name = "test"
        with database_connect:
            database_connect.execute_sql(f"SELECT name AS 名称 FROM {table_name};")
            results = database_connect.get_results()
            ObjectUtil.print_object(results)

    def test_oracle_connect(self):
        database_connect = DatabaseUtil.get_database_connect(ip='192.168.20.23', port=1521, database_name='spm',
                                                             username='rpa_scene_mock', password='rpa_scene_mock',
                                                             oracle_client_path=self.get_test_file("11g"))
        table_name = "ZN物资直接入库查询"
        with database_connect:
            database_connect.execute_sql(f"SELECT * FROM {table_name}")
            results = database_connect.get_results()
            ObjectUtil.print_object(results)

    def test_get_sqlite_connect(self):
        database_connect = DatabaseUtil.get_database_connect(sqlite_path=self.get_test_file("测试.sqlite"))
        table_name = "Test"
        with database_connect:
            database_connect.execute_sql(f"SELECT * FROM {table_name};")
            results = database_connect.get_results()
            ObjectUtil.print_object(results)
