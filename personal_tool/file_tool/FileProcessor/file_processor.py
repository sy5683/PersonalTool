from enum import Enum

from common_util.file_util.file_util.file_util import FileUtil
from file_rocessor.compress_file import CompressFile


class Operations(Enum):
    compress = CompressFile.compress
    decompress = CompressFile.decompress


class FileProcessor:
    """文件处理"""

    def __init__(self):
        self.file_paths = FileUtil.get_file_paths()

    def main(self, function):
        if self.file_paths:
            function(self.file_paths)


if __name__ == '__main__':
    file_processor = FileProcessor()
    # file_processor.main(Operations.compress)
    file_processor.main(Operations.decompress)
