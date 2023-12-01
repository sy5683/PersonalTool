import unittest
from pathlib import Path

from common_util.file_util.zip_util.zip_util import ZipUtil


class ZipUtilTestCase(unittest.TestCase):

    def setUp(self):
        self.test_path = Path(__file__).parent.joinpath("测试.zip")

    def test_decompress(self):
        decompress_paths = ZipUtil.decompress(self.test_path, password="123456")
        for decompress_path in decompress_paths:
            print(decompress_path)
