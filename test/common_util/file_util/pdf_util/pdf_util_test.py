
import unittest
from pathlib import Path

from common_util.file_util.pdf_util.pdf_util import PdfUtil


class PdfUtilTestCase(unittest.TestCase):

    def setUp(self):
        self.pdf_path = Path(__file__).parent.joinpath("测试.pdf")
        self.image_path = Path(__file__).parent.joinpath("测试.png")

    def test_pdf_to_images(self):
        image_paths = PdfUtil.pdf_to_images(self.pdf_path)
        for image_path in image_paths:
            print(image_path)

    def test_images_to_pdf(self):
        image_paths = [self.image_path]
        pdf_path = PdfUtil.images_to_pdf(image_paths)
        print(pdf_path)
