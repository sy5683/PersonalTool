from pathlib import Path


class FileFeature:

    @staticmethod
    def get_file_path(file_name: str = '') -> Path:
        file_path = Path(__file__).parent.parent.joinpath("file")
        return file_path.joinpath(file_name)
