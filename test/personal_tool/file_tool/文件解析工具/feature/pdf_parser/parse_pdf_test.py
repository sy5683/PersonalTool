from common_core.base.test_base import TestBase
from common_util.data_util.object_util.object_util import ObjectUtil
from personal_tool.file_tool.文件解析工具.feature.pdf_parser.parse_pdf import ParsePdf


class ParsePdfTestCase(TestBase):

    def setUp(self):
        self.excel_path = self.get_test_file("江西大唐国际寻乌风电有限责任公司 工商银行 202207.pdf")

    def test_parse_statement(self):
        result = ParsePdf.parse_receipt(self.excel_path)
        ObjectUtil.print_object(result)
