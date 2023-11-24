from enum import Enum

from file_process.feature.file_feature import FileFeature
from file_process.file_decompress import FileDecompress


class Operations(Enum):
    decompress = FileDecompress.file_decompress


class FileProcess:
    """文件处理"""

    def __init__(self):
        self.file_paths = FileFeature.get_file_paths()

    def main(self):
        """"""


if __name__ == '__main__':
    file_process = FileProcess()
    file_process.main()
