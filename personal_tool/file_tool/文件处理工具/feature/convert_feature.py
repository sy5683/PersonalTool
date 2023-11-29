import os
import re
import typing

from common_util.file_util.excel_util.excel_util import ExcelUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil
from common_util.file_util.word_util.word_util import WordUtil


class ConvertFeature:

    @staticmethod
    def to_excel(file_paths: typing.Tuple[str, ...]):
        """转换为excel"""
        for file_path in file_paths:
            _, suffix = os.path.splitext(file_path)
            if re.match(r"\.doc$|\.docx$", suffix):
                WordUtil.word_to_excel(file_path)

    @staticmethod
    def to_image(file_paths: typing.Tuple[str, ...]):
        """转换为图片"""
        for file_path in file_paths:
            _, suffix = os.path.splitext(file_path)
            if re.match(r"\.xlsx$", suffix):
                ExcelUtil.excel_to_images(file_path)
            elif re.match(r"\.pdf$", suffix):
                PdfUtil.pdf_to_images(file_path)

    @staticmethod
    def to_pdf(file_paths: typing.Tuple[str, ...]):
        """转换为pdf"""
        image_paths = []
        for file_path in file_paths:
            _, suffix = os.path.splitext(file_path)
            if re.match(r"\.png$|\.jpg$", suffix):
                image_paths.append(file_path)
        if image_paths:
            PdfUtil.images_to_pdf(image_paths, f"{os.path.splitext(image_paths[0])[0]}.pdf")
