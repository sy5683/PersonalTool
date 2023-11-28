from enum import Enum

from common_util.file_util.file_util.file_util import FileUtil
from file_process.file_decompress import FileDecompress


class Operations(Enum):
    decompress = FileDecompress.decompress


class FileProcess:
    """文件处理"""

    def __init__(self):
        self.file_paths = FileUtil.get_file_paths()

    def main(self, function):
        if self.file_paths:
            function(self.file_paths)


if __name__ == '__main__':
    file_process = FileProcess()
    file_process.main(Operations.decompress)
