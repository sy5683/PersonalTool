import unittest
from pathlib import Path

from common_util.file_util.file_util.file_util import FileUtil


class FileUtilTestCase(unittest.TestCase):

    def setUp(self):
        self.image_path = Path(__file__).parent.joinpath("测试.png")

    def test_format_path(self):
        file_path = FileUtil.format_path(self.image_path)
        print(file_path)

    def test_get_file_original_type(self):
        file_original_type = FileUtil.get_original_type(self.image_path)
        print(file_original_type)
