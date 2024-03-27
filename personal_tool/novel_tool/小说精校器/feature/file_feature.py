from pathlib import Path

from common_util.file_util.file_util.file_util import FileUtil


class FileFeature:

    @staticmethod
    def get_file_path(file_name: str = '') -> str:
        file_dir_path = Path(__file__).parent.parent.joinpath("file")
        FileUtil.make_dir(file_dir_path)
        return str(file_dir_path.joinpath(file_name))
