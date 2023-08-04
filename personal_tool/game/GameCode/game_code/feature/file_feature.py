from pathlib import Path


class FileFeature:

    @classmethod
    def to_database_path(cls, database_name: str = '') -> Path:
        return cls._to_project_path().joinpath(f"database\\{database_name}")

    @staticmethod
    def _to_project_path() -> Path:
        return Path(__file__).parent.parent
