from pathlib import pathlib.Path


class FileFeature:

    @staticmethod
    def get_file_path(file_name: str = '') -> pathlib.Path:
        file_path = pathlib.Path(__file__).parent.parent.joinpath("file")
        return file_path.joinpath(file_name)
