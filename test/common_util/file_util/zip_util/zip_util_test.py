from common_core.base.test_base import TestBase
from common_util.file_util.zip_util.zip_util import ZipUtil


class ZipUtilTestCase(TestBase):

    def setUp(self):
        self.test_path = self.get_test_file("测试.GIF")

    def test_compress(self):
        compress_path = ZipUtil.compress(self.test_path)
        print(compress_path)

    def test_decompress(self):
        decompress_paths = ZipUtil.decompress(self.test_path, password='123456')
        for decompress_path in decompress_paths:
            print(decompress_path)
