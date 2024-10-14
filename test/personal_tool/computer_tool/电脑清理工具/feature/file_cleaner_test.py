from common_core.base.test_base import TestBase
from personal_tool.computer_tool.电脑清理工具.feature.file_cleaner import FileCleaner


class FileCleanerTestCase(TestBase):

    def setUp(self):
        self.dir_path = self.get_test_file("测试")

    def test_clean_dir(self):
        FileCleaner._clean_dir(self.dir_path)
