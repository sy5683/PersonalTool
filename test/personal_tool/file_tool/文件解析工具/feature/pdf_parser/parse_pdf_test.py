from common_core.base.test_base import TestBase
from common_util.data_util.object_util.object_util import ObjectUtil
from personal_tool.file_tool.文件解析工具.feature.pdf_parser.parse_pdf import ParsePdf


class ParsePdfTestCase(TestBase):

    def setUp(self):
        self.pdf_path = self.get_test_file("input")

    def test_parse_statement(self):
        for pdf_path in self.pdf_path.rglob("*.pdf"):
            result = ParsePdf.parse_receipt(pdf_path)
            print([each.__dict__ for each in result.receipts])
