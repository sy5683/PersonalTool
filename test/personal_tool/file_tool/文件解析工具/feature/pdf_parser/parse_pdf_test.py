import re

from common_core.base.test_base import TestBase
from common_util.data_util.object_util.object_util import ObjectUtil
from personal_tool.file_tool.文件解析工具.feature.pdf_parser.parse_pdf import ParsePdf


class ParsePdfTestCase(TestBase):

    def setUp(self):
        self.pdf_path = self.get_test_file("input")

    def test_parse_receipt(self):
        for pdf_path in self.pdf_path.rglob("*"):
            if not re.search("pdf|xps", pdf_path.suffix):
                continue
            result = ParsePdf.parse_receipt(pdf_path)
            for receipt in result.receipts:
                print(receipt.__dict__)
            print()
