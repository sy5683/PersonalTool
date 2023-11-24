from enum import Enum

from file_converter.excel_converter import ExcelConverter
from file_converter.feature.file_feature import FileFeature
from file_converter.pdf_converter import PdfConverter
from file_converter.util.win32_util import Win32Util
from file_converter.word_converter import WordConverter


class Operations(Enum):
    pdf_to_images = PdfConverter.pdf_to_images
    images_to_pdf = PdfConverter.images_to_pdf
    excel_to_images = ExcelConverter.excel_to_images
    word_to_excel = WordConverter.word_to_excel


class FileConverter:
    """文件转换器"""

    def __init__(self):
        self.file_paths = FileFeature.get_file_paths()

    def main(self, function, **kwargs):
        if self.file_paths:
            function(**kwargs)
            Win32Util.open_file(FileFeature.get_save_path())


if __name__ == '__main__':
    file_converter = FileConverter()
    file_converter.main(Operations.word_to_excel)
