import logging
import sqlite3
import typing
from pathlib import Path

from .base.database_connect import DatabaseConnect


class SqliteConnect(DatabaseConnect):

    def __init__(self, sqlite_path: typing.Union[Path, str]):
        self.sqlite_path = str(sqlite_path)
        super().__init__(f"【SQLite】{Path(sqlite_path).name}")

    def _get_connect(self):
        """获取连接"""
        logging.info(f"连接数据库: {self.sqlite_path}")
        self.connect = sqlite3.connect(self.sqlite_path)
        self.cursor = self.connect.cursor()
