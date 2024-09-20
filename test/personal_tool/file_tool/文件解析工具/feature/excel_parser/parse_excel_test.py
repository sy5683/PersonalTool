import re
import typing
from pathlib import Path

from common_core.base.test_base import TestBase
from personal_tool.file_tool.文件解析工具.feature.excel_parser.parse_excel import ParseExcel


class ParseExcelTestCase(TestBase):

    def setUp(self):
        self.statement_path = Path(r"E:\Document\公司文档\RPA\场景文档\02_银行对账\银行流水")

    def test_parse_statement(self):
        statement_path = self.statement_path.joinpath("")
        for excel_path in self.__get_excel_path(statement_path):
            statement_parser = ParseExcel.parse_statement(excel_path)
            for statement in statement_parser.statements:
                print(statement.__dict__)
            print()

    @staticmethod
    def __get_excel_path(pdf_path: Path) -> typing.List[Path]:
        return [each for each in pdf_path.rglob("*") if re.search("xls", each.suffix)]
