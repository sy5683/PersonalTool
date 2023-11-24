from enum import Enum

from file_format.anime_format import AnimeFormat
from file_format.feature.file_feature import FileFeature
from file_format.manga_format import MangaFormat
from file_format.util.win32_util import Win32Util


class Operations(Enum):
    anime_format = AnimeFormat.anime_format
    manga_format = MangaFormat.manga_format


class FileFormat:
    """文件名格式化"""

    def __init__(self):
        self.directory_path = FileFeature.get_directory_path()

    def main(self, function, **kwargs):
        if self.directory_path:
            function(**kwargs)
            Win32Util.open_file(self.directory_path)


if __name__ == '__main__':
    file_format = FileFormat()
    # file_format.main(Operations.anime_format)
    file_format.main(Operations.manga_format, start_number=1)
