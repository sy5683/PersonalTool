from pathlib import Path

from common_util.file_util.file_util.file_util import FileUtil


class FileFeature:

    @staticmethod
    def get_file_path(file_name: str = '') -> Path:
        file_path = Path(__file__).parent.parent.joinpath(f"file/{file_name}")
        FileUtil.make_dir(file_path)
        return file_path

    @classmethod
    def get_image_path(cls, file_name: str = ''):
        return cls.get_file_path(f"image/{file_name}")