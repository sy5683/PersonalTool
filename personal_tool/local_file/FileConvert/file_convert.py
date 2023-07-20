from enum import Enum

import win32api

from file_convert.excel_convert import ExcelConvert
from file_convert.feature.file_feature import FileFeature
from file_convert.pdf_convert import PdfConvert


class Operations(Enum):
    pdf_to_images = PdfConvert.pdf_to_images
    images_to_pdf = PdfConvert.images_to_pdf
    excel_to_images = ExcelConvert.excel_to_images


class FileConvert:

    def main(self, function=None, **kwargs):
        if function and FileFeature.get_file_paths():
            function(**kwargs)
            # 打开结果文件夹
            win32api.ShellExecute(0, "open", FileFeature.get_save_path(), "", "", 1)


if __name__ == '__main__':
    file_convert = FileConvert()
    file_convert.main(Operations.excel_to_images)
