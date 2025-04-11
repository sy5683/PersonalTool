from common_core.base.test_base import TestBase
from common_util.file_util.file_util.file_util import FileUtil


class FileUtilTestCase(TestBase):

    def setUp(self):
        self.file_path = self.get_test_file("测试.png")

    def test_format_path(self):
        file_path = FileUtil.format_path(self.file_path)
        print(file_path)

    def test_get_file_paths(self):
        file_paths = FileUtil.get_file_paths()
        self.assertNotEqual(file_paths, None)
        print(file_paths)

    def test_get_original_type(self):
        file_original_type = FileUtil.get_original_type(self.file_path)
        print(file_original_type)

    def test_get_root_paths(self):
        root_paths = FileUtil.get_root_paths()
        self.assertNotEqual(root_paths, None)
        print(root_paths)

    def test_wait_file_appear(self):
        self.file_path = r"E:\新建文件夹\新建 文本文档.txt"
        FileUtil.wait_file_appear(self.file_path, wait_seconds=10)
