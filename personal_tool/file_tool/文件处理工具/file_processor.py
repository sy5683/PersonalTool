import logging
from enum import Enum

from common_core.base.tool_base import ToolBase
from common_util.file_util.file_util.file_util import FileUtil
from feature.compress_feature import CompressFeature


class Operations(Enum):
    decompress = CompressFeature.decompress


class FileProcessor(ToolBase):

    def __init__(self):
        self.file_paths = FileUtil.get_file_paths()

    def main(self, function, **kwargs):
        if self.file_paths:
            function(self.file_paths, **kwargs)
        else:
            logging.info("未选择文件")


if __name__ == '__main__':
    file_processor = FileProcessor()
    file_processor.main(Operations.decompress, password="123456")
