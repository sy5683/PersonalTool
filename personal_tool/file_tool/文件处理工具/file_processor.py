from enum import Enum

from common_core.base.tool_base import ToolBase
from common_util.file_util.file_util.file_util import FileUtil
from feature.compress_feature import CompressFeature
from feature.convert_feature import ConvertFeature


class Operations(Enum):
    compress_pdf_size = CompressFeature.compress_pdf_size
    decompress = CompressFeature.decompress
    to_excel = ConvertFeature.to_excel
    to_image = ConvertFeature.to_image
    to_pdf = ConvertFeature.to_pdf


class FileProcessor(ToolBase):

    def __init__(self):
        super().__init__()
        self.file_paths = FileUtil.get_file_paths()
        assert self.file_paths, "未选择文件"

    def main(self, function, **kwargs):
        function(self.file_paths, **kwargs)


if __name__ == '__main__':
    file_processor = FileProcessor()
    file_processor.main(Operations.compress_pdf_size, dpi=100)
    # file_processor.main(Operations.decompress, password=None)
    # file_processor.main(Operations.to_excel)
    # file_processor.main(Operations.to_image)
    # file_processor.main(Operations.to_pdf)
