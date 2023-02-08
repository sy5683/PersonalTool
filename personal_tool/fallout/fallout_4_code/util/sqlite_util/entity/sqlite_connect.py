import logging
import sqlite3
import traceback
from pathlib import Path
from sqlite3 import Connection, Cursor
from typing import Union, List


class SqliteConnect:

    def __init__(self, sqlite_name: str):
        self.sqlite_name = sqlite_name  # 数据库名
        self.sqlite_path = Path(__file__).parent.parent.parent.parent.joinpath(f"database\\{sqlite_name}")
        self.connect: Union[Connection, None] = None
        self.cursor: Union[Cursor, None] = None

    def sql_execute(self, sql: str):
        """执行sql"""
        self._sqlite_connect()
        # noinspection PyBroadException
        try:
            self.cursor.execute(sql)  # 执行sql
            self.connect.commit()  # 提交事务，只有运行了这句话，sql操作才会生效
        except Exception:
            logging.warning(traceback.format_exc())
            self.connect.rollback()  # 回滚操作

    def get_result(self) -> List[tuple]:
        self._sqlite_connect()
        return self.cursor.fetchall()

    def close(self):
        if self.cursor is not None:
            self.cursor.close()  # 关闭游标
            self.cursor = None
        if self.connect is not None:
            self.connect.close()  # 关闭连接
            self.connect = None

    def _sqlite_connect(self):
        if self.connect is None:
            self.connect = sqlite3.connect(str(self.sqlite_path))  # 连接sqlite_path数据库
            self.cursor = self.connect.cursor()  # 得到一个可以执行SQL语句的游标对象
