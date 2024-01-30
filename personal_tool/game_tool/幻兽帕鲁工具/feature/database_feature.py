from pathlib import Path

from common_util.code_util.database_util.database_util import DatabaseUtil


class DatabaseFeature:
    _database_connect = None

    @classmethod
    def get_database_connect(cls):
        if cls._database_connect is None:
            sqlite_path = Path(__file__).parent.parent.joinpath("file\\pal_world_database.sqlite")
            assert sqlite_path.exists(), f"SQLite数据库不存在: {sqlite_path}"
            cls._database_connect = DatabaseUtil.get_database_connect(sqlite_path=sqlite_path)
        return cls._database_connect
