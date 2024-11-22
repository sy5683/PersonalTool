from enum import Enum

from common_core.base.tool_base import ToolBase
from common_util.data_util.object_util.object_util import ObjectUtil
from common_util.file_util.file_util.file_util import FileUtil
from feature.excel_parser.parse_excel import ParseExcel
from personal_tool.file_tool.文件解析工具.feature.pdf_parser.parse_pdf import ParsePdf


class Operations(Enum):
    parse_statement = ParseExcel.parse_statement
    parse_receipt = ParsePdf.parse_receipt
    parse_voucher = ParsePdf.parse_voucher


class FileParser(ToolBase):

    def __init__(self):
        super().__init__()
        self.file_path = FileUtil.get_file_path()
        assert self.file_path, "未选择文件"

    def main(self, function, **kwargs):
        result = function(self.file_path, **kwargs)
        ObjectUtil.print_object(result)


if __name__ == '__main__':
    file_parser = FileParser()
    # file_parser.main(Operations.parse_statement)
    file_parser.main(Operations.parse_receipt)
    # file_parser.main(Operations.parse_voucher)
