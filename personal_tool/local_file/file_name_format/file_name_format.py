import win32api

from base.tool_base import ToolBase
from cache.path_cache import PathCache
from feature.format_feature import FormatFeature


class FileNameFormat(ToolBase):
    """文件名格式化"""

    def __init__(self):
        self.directory_path = PathCache.get_directory_path()  # 初始化获取文件路径

    def main(self, function=None, **kwargs):
        if self.directory_path:
            if function:
                function(**kwargs)
            # 打开结果文件夹
            win32api.ShellExecute(0, "open", str(self.directory_path), "", "", 1)

    def _directory_path_verification(self):
        """文件校验"""


if __name__ == '__main__':
    file_name_format = FileNameFormat()
    # file_name_format.main(FormatFeature.anime_format)
    file_name_format.main(FormatFeature.manga_format, start_number=1)
