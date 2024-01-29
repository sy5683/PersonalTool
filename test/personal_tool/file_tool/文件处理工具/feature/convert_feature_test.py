from common_core.base.test_base import TestBase
from personal_tool.file_tool.文件处理工具.feature.convert_feature import ConvertFeature


class ConvertFeatureTestCase(TestBase):

    def setUp(self):
        self.excel_paths = (str(self.get_test_file("测试.xlsx")),)
        self.image_paths = (str(self.get_test_file("测试_1.png")), str(self.get_test_file("测试_2.png")))
        self.pdf_paths = (str(self.get_test_file("测试.pdf")),)

    def test_to_image(self):
        ConvertFeature.to_image(self.excel_paths)

    def test_to_pdf(self):
        ConvertFeature.to_pdf(self.image_paths)
