from common_util.system_util.database_util.database_util import DatabaseUtil
from common_util.system_util.database_util.database_utils.entity.base.database_connect import DatabaseConnect
from ...file_feature import FileFeature


class DatabaseConnectFeature:
    _database_connect = None

    @classmethod
    def get_database_connect(cls) -> DatabaseConnect:
        if cls._database_connect is None:
            database_path = FileFeature.get_file_path("database\\AircraftWar.sqlite")
            cls._database_connect = DatabaseUtil.get_database_connect(sqlite_path=database_path)
        return cls._database_connect
