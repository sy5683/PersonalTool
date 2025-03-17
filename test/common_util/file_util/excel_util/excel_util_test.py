import openpyxl

from common_core.base.test_base import TestBase
from common_util.data_util.object_util.object_util import ObjectUtil
from common_util.file_util.excel_util.excel_util import ExcelUtil
from common_util.file_util.file_util.file_util import FileUtil


class ExcelUtilTestCase(TestBase):

    def setUp(self):
        self.excel_path = self.get_test_file("测试.xlsx")

    def test_excel_to_images(self):
        image_paths = ExcelUtil.excel_to_images(self.excel_path)
        FileUtil.open_file(image_paths[0])

    def test_format_date_data(self):
        # date_data = ExcelUtil.format_date_data("42141.0")
        date_data = ExcelUtil.format_date_data("2024-08-16")
        self.assertNotEqual(date_data, None)
        print(date_data)

    def test_format_int_data(self):
        int_data = ExcelUtil.format_int_data(1.2)
        self.assertNotEqual(int_data, None)
        print(int_data)

    def test_get_data_list(self):
        data_list = ExcelUtil.get_data_list(self.excel_path, tag_row_quantity=2)
        ObjectUtil.print_object(data_list)

    def test_set_cell(self):
        workbook = openpyxl.load_workbook(self.excel_path)
        worksheet = workbook.active
        cell = worksheet['C2']
        ExcelUtil.set_cell(cell, horizontal=None)
        workbook.save(self.excel_path)
        workbook.close()

    def test_xls_to_xlsx(self):
        excel_path = ExcelUtil.xls_to_xlsx(self.excel_path)
        print(excel_path)
