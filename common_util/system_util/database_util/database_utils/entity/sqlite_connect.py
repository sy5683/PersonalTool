import sqlite3
import typing

from .base.database_connect import DatabaseConnect


class SqliteConnect(DatabaseConnect):

    def __init__(self, sqlite_path: typing.Union[pathlib.Path, str]):
        self.sqlite_path = str(sqlite_path)
        super().__init__(f"【SQLite】{pathlib.Path(sqlite_path).name}")

    def _get_connect(self):
        """连接数据库"""
        self.connect = sqlite3.connect(self.sqlite_path)
        self.cursor = self.connect.cursor()
