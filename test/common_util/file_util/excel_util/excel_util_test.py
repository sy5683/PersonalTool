import unittest
from pathlib import Path

from common_util.data_util.object_util.object_util import ObjectUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil


class ExcelUtilTestCase(unittest.TestCase):

    def setUp(self):
        self.excel_path = Path(__file__).parent.joinpath("测试.xls")

    def test_format_date_data(self):
        date_data = ExcelUtil.format_date_data("2958465")
        self.assertNotEqual(date_data, None)
        print(date_data)

    def test_format_int_data(self):
        int_data = ExcelUtil.format_int_data(1.2)
        self.assertNotEqual(int_data, None)
        print(int_data)

    def test_get_data_list(self):
        data_list = ExcelUtil.get_data_list(self.excel_path, tag_row_quantity=2)
        ObjectUtil.print_object(data_list)

    def test_xls_to_xlsx(self):
        excel_path = ExcelUtil.xls_to_xlsx(self.excel_path)
        print(excel_path)
