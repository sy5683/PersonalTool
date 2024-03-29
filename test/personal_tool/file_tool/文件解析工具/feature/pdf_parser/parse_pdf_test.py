import re
import typing
from pathlib import Path

from common_core.base.test_base import TestBase
from personal_tool.file_tool.文件解析工具.feature.pdf_parser.parse_pdf import ParsePdf


class ParsePdfTestCase(TestBase):

    def setUp(self):
        self.receipt_path = Path(r"E:\Document\公司文档\先一科技\RPA\场景文档\01_银行回单补扫\回单")

    def test_parse_receipt(self):
        receipt_path = self.receipt_path.joinpath("")
        for pdf_path in self.__get_pdf_path(receipt_path):
            result = ParsePdf.parse_receipt(pdf_path)
            for receipt in result.receipts:
                print(receipt.__dict__)
            print()

    @staticmethod
    def __get_pdf_path(pdf_path: Path) -> typing.List[Path]:
        return [each for each in pdf_path.rglob("*") if re.search("pdf|xps", each.suffix)]
