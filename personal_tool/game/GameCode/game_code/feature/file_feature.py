from pathlib import Path


class FileFeature:

    @staticmethod
    def to_database_path(database_name: str = '') -> Path:
        return Path(__file__).parent.parent.joinpath(f"database\\{database_name}")
