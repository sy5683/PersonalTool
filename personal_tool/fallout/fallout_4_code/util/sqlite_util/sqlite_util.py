from .entity.sqlite_connect import SqliteConnect


class SqliteUtil:
    _sqlite_map = {}

    @classmethod
    def get_sqlite_connect(cls, sqlite_name: str) -> SqliteConnect:
        if sqlite_name not in cls._sqlite_map:
            sqlite_connect = SqliteConnect(sqlite_name)
            cls._sqlite_map[sqlite_name] = sqlite_connect
        return cls._sqlite_map.get(sqlite_name)
