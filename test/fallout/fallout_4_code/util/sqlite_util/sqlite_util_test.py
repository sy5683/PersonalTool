import unittest

from personal_tool.fallout.fallout_4_code.config.fallout_4_code_config import sqlite_name, table_name
from personal_tool.fallout.fallout_4_code.util.sqlite_util.sqlite_util import SqliteUtil


class SqliteUtilTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.sqlite_connect = SqliteUtil.get_sqlite_connect(sqlite_name)

    def test_create(self):
        create_sql = f"CREATE TABLE {table_name} (id INTEGER(10) PRIMARY KEY, item_name VARCHAR(20)," \
                     f" item_code VARCHAR(20), usage_count INT(5) NOT NULL DEFAULT 0);"
        self.sqlite_connect.sql_execute(create_sql)

    def tearDown(self) -> None:
        self.sqlite_connect.close()
