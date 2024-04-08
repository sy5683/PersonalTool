import os
import re
import typing

from common_util.code_util.win32_util.win32_util import Win32Util
from common_util.file_util.excel_util.excel_util import ExcelUtil
from common_util.file_util.file_util.file_util import FileUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil
from common_util.file_util.word_util.word_util import WordUtil


class ConvertFeature:

    @staticmethod
    def to_excel(file_paths: typing.Tuple[str, ...]):
        """转换为excel"""
        for file_path in file_paths:
            original_type = FileUtil.get_original_type(file_path)
            if re.match(r"docx$", original_type):
                excel_path = WordUtil.word_to_excel(file_path)
            else:
                continue
            Win32Util.open_file(excel_path)

    @staticmethod
    def to_image(file_paths: typing.Tuple[str, ...]):
        """转换为图片"""
        for file_path in file_paths:
            original_type = FileUtil.get_original_type(file_path)
            if re.match(r"xlsx$", original_type):
                image_paths = ExcelUtil.excel_to_images(file_path)
            elif re.match(r"pdf$", original_type):
                image_paths = PdfUtil.pdf_to_images(file_path)
            elif re.match(r"doc$|docx$", original_type):
                # 因为没有直接将word转换为图片的方法，因此先实现word转pdf，再将pdf转图片
                pdf_path = WordUtil.word_to_pdf(file_path)
                image_paths = PdfUtil.pdf_to_images(pdf_path)
                os.remove(pdf_path)
            else:
                continue
            Win32Util.open_file(os.path.dirname(image_paths[0]))

    @staticmethod
    def to_pdf(file_paths: typing.Tuple[str, ...]):
        """转换为pdf"""
        image_paths = []
        word_paths = []
        for file_path in file_paths:
            original_type = FileUtil.get_original_type(file_path)
            if re.match(r"png$|jpg$", original_type):
                image_paths.append(file_path)
            elif re.match(r"doc$|docx$", original_type):
                word_paths.append(file_path)
        if image_paths:
            pdf_path = PdfUtil.images_to_pdf(image_paths)
            Win32Util.open_file(pdf_path)
        for word_path in word_paths:
            pdf_path = WordUtil.word_to_pdf(word_path)
            Win32Util.open_file(pdf_path)
