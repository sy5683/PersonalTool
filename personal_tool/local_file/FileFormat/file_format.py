from enum import Enum

import win32api

from file_format.anime_format import AnimeFormat
from file_format.feature.file_feature import FileFeature
from file_format.manga_format import MangaFormat


class Operations(Enum):
    anime_format = AnimeFormat.anime_format
    manga_format = MangaFormat.manga_format


class FileFormat:
    """文件名格式化"""

    def main(self, function=None, **kwargs):
        if function and FileFeature.get_directory_path():
            function(**kwargs)
            # 打开结果文件夹
            win32api.ShellExecute(0, "open", str(FileFeature.get_directory_path()), "", "", 1)


if __name__ == '__main__':
    file_format = FileFormat()
    # file_format.main(Operations.anime_format)
    file_format.main(Operations.manga_format, start_number=109)
