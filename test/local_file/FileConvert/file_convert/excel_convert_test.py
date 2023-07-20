import unittest

from pathlib import Path

import win32api

from personal_tool.local_file.FileConvert.file_convert.excel_convert import ExcelConvert
from personal_tool.local_file.FileConvert.file_convert.feature.file_feature import FileFeature


class ExcelConvertTestCase(unittest.TestCase):

    def test_excel_to_images(self):
        FileFeature._file_paths = [str(Path(__file__).parent.joinpath("test.xlsx"))]
        self.assertEqual(ExcelConvert.excel_to_images(), None)

    def tearDown(self) -> None:
        win32api.ShellExecute(0, "open", FileFeature.get_save_path(), "", "", 1)
