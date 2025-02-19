from enum import Enum

from common_core.base.tool_base import ToolBase
from feature.file_feature import FileFeature
from feature.format_feature import FormatFeature


class Operations(Enum):
    format_coding = FormatFeature.format_coding
    format_color = FormatFeature.format_color


class CodingMarker(ToolBase):

    def __init__(self, file_name: str):
        super().__init__()
        self.dir_path = FileFeature.get_file_path(file_name)
        assert self.dir_path, f"文件不存在或路径不正确: {file_name}"

    def main(self, function, **kwargs):
        function(self.dir_path, **kwargs)


if __name__ == '__main__':
    coding_marker = CodingMarker("")
    coding_marker.main(Operations.format_color)
