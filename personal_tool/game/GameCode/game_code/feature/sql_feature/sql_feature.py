import logging
from typing import List, Tuple

from .entity.sql_connect import SqlConnect


class SqlFeature:
    _sql_connect = None
    _table_name = "fallout4_code"

    @classmethod
    def find_item(cls, item_name: str) -> Tuple[str, str]:
        """查找道具"""
        sql = f"SELECT item_name, item_code FROM {cls._table_name} WHERE item_name='{item_name}';"
        results = cls._get_connect().select(sql)
        if results:
            return results[0]

    @classmethod
    def find_items(cls, item_name: str = None) -> List[Tuple[str, str]]:
        sql = f"SELECT item_name, item_code FROM {cls._table_name} "
        if item_name:
            sql += f"WHERE item_name LIKE '%{item_name}%';"
        else:
            sql += "ORDER BY usage_count DESC;"
        return cls._get_connect().select(sql)

    @classmethod
    def add_usage_count(cls, item_name: str):
        sql = f"UPDATE {cls._table_name} SET usage_count=usage_count+1 WHERE item_name='{item_name}';"
        cls._get_connect().update(sql)

    @classmethod
    def add_item(cls, item_name: str, item_code: str):
        """添加道具"""
        sql = f"INSERT INTO {cls._table_name} (item_name, item_code) VALUES ('{item_name}', '{item_code}');"
        cls._get_connect().insert(sql)

    @classmethod
    def connect_close(cls):
        if cls._sql_connect:
            cls._sql_connect.close()
            cls._sql_connect = None

    @classmethod
    def _get_connect(cls) -> SqlConnect:
        if cls._sql_connect is None:
            cls._sql_connect = SqlConnect()
        return cls._sql_connect
