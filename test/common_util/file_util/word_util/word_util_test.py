from common_core.base.test_base import TestBase
from common_util.file_util.word_util.word_util import WordUtil


class WordUtilTestCase(TestBase):

    def setUp(self):
        self.test_path = self.get_test_file("测试.docx")

    def test_decompress(self):
        excel_path = WordUtil.word_to_excel(self.test_path)
        print(excel_path)
