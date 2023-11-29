import unittest
from pathlib import Path

from personal_tool.file_tool.文件处理工具.feature.convert_feature import ConvertFeature


class ConvertFeatureTestCase(unittest.TestCase):

    def setUp(self):
        self.excel_paths = (str(Path(__file__).parent.joinpath("测试.xlsx")),)
        self.image_paths = (str(Path(__file__).parent.joinpath("测试_1.png")),
                            str(Path(__file__).parent.joinpath("测试_2.png")))
        self.pdf_paths = (str(Path(__file__).parent.joinpath("测试.pdf")),)

    def test_to_image(self):
        ConvertFeature.to_image(self.excel_paths)

    def test_to_pdf(self):
        ConvertFeature.to_pdf(self.image_paths)
