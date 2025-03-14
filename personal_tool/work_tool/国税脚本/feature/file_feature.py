from pathlib import Path

from common_util.file_util.file_util.file_util import FileUtil


class FileFeature:

    @staticmethod
    def get_file_path(file_name: str = '') -> Path:
        file_path = Path(__file__).parent.parent.joinpath("file")
        FileUtil.make_dir(file_path)
        return file_path.joinpath(file_name)
