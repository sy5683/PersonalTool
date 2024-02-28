from common_core.base.test_base import TestBase
from common_util.data_util.object_util.object_util import ObjectUtil
from personal_tool.file_tool.文件解析工具.feature.excel_parser.parse_excel import ParseExcel


class ParseExcelTestCase(TestBase):

    def setUp(self):
        self.excel_path = self.get_test_file("广东大唐国际潮州发电有限责任公司 财务公司 202011.xls")

    def test_parse_statement(self):
        statement_parser = ParseExcel.parse_statement(self.excel_path)
        ObjectUtil.print_object(statement_parser)
