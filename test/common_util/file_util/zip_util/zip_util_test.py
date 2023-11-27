
import unittest
from pathlib import Path

from common_util.file_util.zip_util.zip_util import ZipUtil


class ZipUtilTestCase(unittest.TestCase):

    def setUp(self):
        self.test_path = Path(__file__).parent.joinpath("测试.zip")

    def test_decompress(self):
        ZipUtil.decompress(self.test_path)
