from .database_utils.connect_database import ConnectDatabase
from .database_utils.entity.base.database_connect import DatabaseConnect


class DatabaseUtil:

    @staticmethod
    def get_database_connect(**kwargs) -> DatabaseConnect:
        """获取数据库连接"""
        return ConnectDatabase.get_database_connect(**kwargs)
