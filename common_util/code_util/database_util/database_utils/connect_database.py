from .entity.base.database_connect import DatabaseConnect
from .entity.oracle_connect import OracleConnect
from .entity.sqlite_connect import SqliteConnect


class ConnectDatabase:

    @staticmethod
    def get_database_connect(**kwargs) -> DatabaseConnect:
        """获取数据库连接"""
        ip = kwargs.get("ip")
        port = kwargs.get("port")
        username = kwargs.get("username")
        password = kwargs.get("password")
        if all([ip, port, username, password]):
            # Oracle数据库
            database_name = kwargs.get("database_name")
            oracle_client_path = kwargs.get("oracle_client_path")
            if kwargs.get("database_name"):
                return OracleConnect(ip, port, database_name, username, password, str(oracle_client_path))
        # SQLite数据库
        sqlite_path = kwargs.get("sqlite_path")
        if sqlite_path:
            return SqliteConnect(sqlite_path)
        # 判断逻辑无法判断数据库
        raise ValueError(f"未知的数据库信息: {kwargs}")
