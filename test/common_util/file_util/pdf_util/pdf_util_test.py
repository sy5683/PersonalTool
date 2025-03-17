from common_core.base.test_base import TestBase
from common_util.data_util.object_util.object_util import ObjectUtil
from common_util.file_util.file_util.file_util import FileUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil


class PdfUtilTestCase(TestBase):

    def setUp(self):
        self.image_path = self.get_test_file("测试.png")
        self.pdf_path = self.get_test_file("测试.pdf")

    def test_get_pdf_profiles(self):
        pdf_profiles = PdfUtil.get_pdf_profiles(self.pdf_path, 20)
        for pdf_profile in pdf_profiles:
            for table in pdf_profile.tables:
                for row in range(table.max_rows):
                    print(table.get_row_values(row))
            print()
            for pdf_word in pdf_profile.words:
                print(pdf_word.text)
            print()

    def test_get_pdf_words(self):
        pdf_words = PdfUtil.get_pdf_words(self.pdf_path, 20)
        ObjectUtil.print_object(pdf_words)

    def test_get_pdf_tables(self):
        pdf_tables = PdfUtil.get_pdf_tables(self.pdf_path)
        ObjectUtil.print_object(pdf_tables)

    def test_pdf_to_images(self):
        image_paths = PdfUtil.pdf_to_images(self.pdf_path)
        FileUtil.open_file(image_paths[0])

    def test_images_to_pdf(self):
        image_paths = [self.image_path]
        pdf_path = PdfUtil.images_to_pdf(image_paths)
        print(pdf_path)
