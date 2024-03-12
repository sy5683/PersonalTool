from .entity.base.database_connect import DatabaseConnect
from .entity.mysql_connect import MysqlConnect
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
            database_name = kwargs.get("database_name")
            # Oracle数据库
            oracle_client_path = kwargs.get("oracle_client_path")
            if oracle_client_path:
                return OracleConnect(ip, port, database_name, username, password, str(oracle_client_path))
            # MySQL数据库
            return MysqlConnect(ip, port, database_name, username, password)
        # SQLite数据库
        sqlite_path = kwargs.get("sqlite_path")
        if sqlite_path:
            return SqliteConnect(sqlite_path)
        # 判断逻辑无法判断数据库
        raise ValueError(f"未知的数据库信息: {kwargs}")
