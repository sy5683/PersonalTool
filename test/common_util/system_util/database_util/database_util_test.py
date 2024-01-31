from common_core.base.test_base import TestBase
from common_util.data_util.object_util.object_util import ObjectUtil
from common_util.system_util.database_util.database_util import DatabaseUtil


class DatabaseUtilTestCase(TestBase):

    def test_get_mysql_connect(self):
        database_connect = DatabaseUtil.get_database_connect(ip='192.168.20.23', port=1521, database_name='spm',
                                                             username='rpa_scene_mock', password='rpa_scene_mock')
        # table_name = "Test"
        # database_connect.execute_sql(f"SELECT name FROM pragma_table_info('{table_name}');")
        # tags = [each[0] for each in database_connect.get_results()]
        # database_connect.execute_sql(f"SELECT * FROM {table_name};")
        # data_list = []
        # for each in database_connect.get_results():
        #     data_list.append(dict(zip(tags, each)))
        # ObjectUtil.print_object(data_list)

    def test_oracle_connect(self):
        database_connect = DatabaseUtil.get_database_connect(ip='192.168.20.23', port=1521, database_name='spm',
                                                             username='rpa_scene_mock', password='rpa_scene_mock',
                                                             oracle_client_path=self.get_test_file("11g"))
        table_name = "ZN物资直接入库查询"
        database_connect.execute_sql(f"select column_name from all_tab_cols where Table_name='{table_name}'")
        tags = [each[0] for each in database_connect.get_results()]
        database_connect.execute_sql(f"SELECT * FROM {table_name}")
        data_list = []
        for each in database_connect.get_results():
            data_list.append(dict(zip(tags, each)))
        ObjectUtil.print_object(data_list)

    def test_get_sqlite_connect(self):
        database_connect = DatabaseUtil.get_database_connect(sqlite_path=self.get_test_file("测试.sqlite"))
        table_name = "Test"
        database_connect.execute_sql(f"SELECT name FROM pragma_table_info('{table_name}');")
        tags = [each[0] for each in database_connect.get_results()]
        database_connect.execute_sql(f"SELECT * FROM {table_name};")
        data_list = []
        for each in database_connect.get_results():
            data_list.append(dict(zip(tags, each)))
        ObjectUtil.print_object(data_list)
