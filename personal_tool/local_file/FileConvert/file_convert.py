from enum import Enum

from file_convert.excel_convert import ExcelConvert
from file_convert.feature.file_feature import FileFeature
from file_convert.pdf_convert import PdfConvert
from file_convert.util.win32_util import Win32Util


class Operations(Enum):
    pdf_to_images = PdfConvert.pdf_to_images
    images_to_pdf = PdfConvert.images_to_pdf
    excel_to_images = ExcelConvert.excel_to_images


class FileConvert:
    """文件转换"""

    def __init__(self):
        self.file_paths = FileFeature.get_file_paths()

    def main(self, function, **kwargs):
        if self.file_paths:
            function(**kwargs)
            Win32Util.open_file(FileFeature.get_save_path())


if __name__ == '__main__':
    file_convert = FileConvert()
    file_convert.main(Operations.excel_to_images)
