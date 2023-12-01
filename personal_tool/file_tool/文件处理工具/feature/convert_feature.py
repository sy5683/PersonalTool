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
            else:
                continue
            Win32Util.open_file(os.path.dirname(image_paths[0]))

    @staticmethod
    def to_pdf(file_paths: typing.Tuple[str, ...]):
        """转换为pdf"""
        image_paths = []
        for file_path in file_paths:
            original_type = FileUtil.get_original_type(file_path)
            if re.match(r"png$|jpg$", original_type):
                image_paths.append(file_path)
        if image_paths:
            pdf_path = PdfUtil.images_to_pdf(image_paths)
            Win32Util.open_file(pdf_path)
