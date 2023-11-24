import unittest

from pathlib import Path

import win32api

from personal_tool.local_file.FileConverter.file_converter.excel_converter import ExcelConverter
from personal_tool.local_file.FileConverter.file_converter.feature.file_feature import FileFeature


class ExcelConverterTestCase(unittest.TestCase):

    def test_excel_to_images(self):
        FileFeature._file_paths = [str(Path(__file__).parent.joinpath("test.xlsx"))]
        self.assertEqual(ExcelConverter.excel_to_images(), None)

    def tearDown(self) -> None:
        win32api.ShellExecute(0, "open", FileFeature.get_save_path(), "", "", 1)
