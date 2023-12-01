import unittest
from pathlib import Path

from common_util.data_util.object_util.object_util import ObjectUtil
from common_util.file_util.zip_util.zip_util import ZipUtil


class ZipUtilTestCase(unittest.TestCase):

    def setUp(self):
        self.test_path = Path(__file__).parent.joinpath("测试.zip")

    def test_decompress(self):
        with open(self.test_path, "rb") as file:
            print(file.read())
        # decompress_paths = ZipUtil.decompress(self.test_path, password="123456")
        # ObjectUtil.print_object(decompress_paths)
