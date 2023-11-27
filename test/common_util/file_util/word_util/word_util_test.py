import unittest
from pathlib import Path

from common_util.file_util.word_util.word_util import WordUtil


class WordUtilTestCase(unittest.TestCase):

    def setUp(self):
        self.test_path = Path(__file__).parent.joinpath("测试.docx")

    def test_decompress(self):
        excel_path = WordUtil.word_to_excel(self.test_path)
        print(excel_path)
