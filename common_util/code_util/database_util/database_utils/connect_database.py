from .entity.base.database_connect import DatabaseConnect
from .entity.sqlite_connect import SqliteConnect


class ConnectDatabase:

    @staticmethod
    def get_database_connect(**kwargs) -> DatabaseConnect:
        """获取数据库连接"""
        sqlite_path = kwargs.get("sqlite_path")
        if sqlite_path:
            return SqliteConnect(sqlite_path)
        raise ValueError(f"未知的数据库信息: {kwargs}")
