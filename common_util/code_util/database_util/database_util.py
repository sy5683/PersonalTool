import typing

from .database_utils.connect_database import ConnectDatabase
from .database_utils.control_table import ControlTable
from .database_utils.entity.base.database_connect import DatabaseConnect


class DatabaseUtil:

    @staticmethod
    def get_data_list(database_connect: DatabaseConnect, table_name: str) -> typing.List[dict]:
        """获取数据库表数据"""
        return ControlTable.get_data_list(database_connect, table_name)

    @staticmethod
    def get_database_connect(**kwargs) -> DatabaseConnect:
        """获取数据库连接"""
        return ConnectDatabase.get_database_connect(**kwargs)
