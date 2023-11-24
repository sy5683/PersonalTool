import unittest
from pathlib import Path

import win32api

from personal_tool.local_file.FileConverter.file_converter.feature.file_feature import FileFeature
from personal_tool.local_file.FileConverter.file_converter.pdf_converter import PdfConverter


class PdfConverterTestCase(unittest.TestCase):

    def test_pdf_to_images(self):
        FileFeature._file_paths = [str(Path(__file__).parent.joinpath("test.pdf"))]
        self.assertEqual(PdfConverter.pdf_to_images(), None)

    def test_images_to_pdf(self):
        FileFeature._file_paths = [str(Path(__file__).parent.joinpath("test_1.png")),
                                   str(Path(__file__).parent.joinpath("test_2.png"))]
        self.assertEqual(PdfConverter.images_to_pdf(), None)

    def tearDown(self) -> None:
        win32api.ShellExecute(0, "open", FileFeature.get_save_path(), "", "", 1)
