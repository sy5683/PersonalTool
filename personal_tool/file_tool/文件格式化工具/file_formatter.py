from enum import Enum
from pathlib import Path

from common_core.base.tool_base import ToolBase
from common_util.code_util.win32_util.win32_util import Win32Util
from common_util.file_util.file_util.file_util import FileUtil
from feature.formatter.anime_formatter import AnimeFormatter
from feature.formatter.manga_formatter import MangaFormatter


class Operations(Enum):
    format_anime_name = AnimeFormatter.format_anime_name
    format_manga_name = MangaFormatter.format_manga_name


class FileFormatter(ToolBase):

    def __init__(self):
        super().__init__()
        self.directory_path = FileUtil.get_directory_path()
        assert self.directory_path, "未选择文件夹"

    def main(self, function, **kwargs):
        function(Path(self.directory_path), **kwargs)
        Win32Util.open_file(self.directory_path)


if __name__ == '__main__':
    file_formatter = FileFormatter()
    # file_formatter.main(Operations.format_anime_name)
    file_formatter.main(Operations.format_manga_name, start_number=1)
