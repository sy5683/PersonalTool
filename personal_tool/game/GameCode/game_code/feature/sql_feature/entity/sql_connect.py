import sqlite3
from contextlib import contextmanager
from typing import List

from ....feature.file_feature import FileFeature


class SqlConnect:

    def __init__(self):
        self.database_path = FileFeature.to_database_path("Fallout4Code.db")
        self.connect = sqlite3.connect(str(self.database_path))  # 连接数据库
        self.cursor = self.connect.cursor()  # 得到一个可以执行SQL语句的游标对象

    def select(self, sql: str) -> List[tuple]:
        """查询"""
        with self._execute(sql):
            return self.cursor.fetchall()

    def update(self, sql: str):
        """更新"""
        with self._execute(sql):
            pass

    def insert(self, sql: str):
        """插入"""
        with self._execute(sql):
            pass

    def close(self):
        if self.cursor is not None:
            self.cursor.close()  # 关闭游标
            self.cursor = None
        if self.connect is not None:
            self.connect.close()  # 关闭连接
            self.connect = None

    @contextmanager
    def _execute(self, sql: str):
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            yield
        except Exception as e:
            self.connect.rollback()
            raise e
