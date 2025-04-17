import pathlib
import typing

import numpy

from .pdf_utils.convert_pdf import ConvertPdf
from .pdf_utils.entity.pdf_element import Table, Word
from .pdf_utils.entity.pdf_profile import PdfProfile, TableProfile
from .pdf_utils.extract_pdf import ExtractPdf
from .pdf_utils.parse_pdf import ParsePdf
from .pdf_utils.process_pdf_profile import ProcessPdfProfile


class PdfUtil:

    @staticmethod
    def filter_word(words: typing.List[Word], pattern: typing.Union[str, typing.Pattern[str]],
                    index: int = 0) -> typing.Union[str, None]:
        """筛选文字"""
        return ProcessPdfProfile.filter_word(words, pattern, index)

    @staticmethod
    def filter_words(words: typing.List[Word], pattern: typing.Union[str, typing.Pattern[str]]) -> typing.List[str]:
        """筛选文字列表"""
        return ProcessPdfProfile.filter_words(words, pattern)

    @staticmethod
    def get_pdf_images(pdf_path: str, page_index: int = None) -> typing.List[numpy.ndarray]:
        """提取pdf中图片"""
        return ExtractPdf.get_pdf_images(pdf_path, page_index)

    @staticmethod
    def get_pdf_profiles(pdf_path: typing.Union[pathlib.Path, str], threshold_x: int = 10) -> typing.List[PdfProfile]:
        """获取pdf内容"""
        return ParsePdf.get_pdf_profiles(str(pdf_path), threshold_x)

    @staticmethod
    def get_pdf_tables(pdf_path: typing.Union[pathlib.Path, str]) -> typing.List[Table]:
        """获取pdf中的表格"""
        return ParsePdf.get_pdf_tables(str(pdf_path))

    @staticmethod
    def get_pdf_words(pdf_path: typing.Union[pathlib.Path, str], threshold_x: int = 10) -> typing.List[Word]:
        """获取pdf中的文字"""
        return ParsePdf.get_pdf_words(str(pdf_path), threshold_x)

    @staticmethod
    def images_to_pdf(image_paths: typing.List[typing.Union[pathlib.Path, str]],
                      save_path: typing.Union[pathlib.Path, str] = None, operate_type: str = 'fitz') -> str:
        """图片转pdf"""
        return ConvertPdf.images_to_pdf([str(image_path) for image_path in image_paths], save_path, operate_type)

    @staticmethod
    def merge_words(words: typing.List[Word], threshold: int = 1) -> typing.List[Word]:
        """合并pdf文字"""
        return ProcessPdfProfile.merge_words(words, threshold)

    @staticmethod
    def pdf_to_images(pdf_path: typing.Union[pathlib.Path, str], save_path: typing.Union[pathlib.Path, str] = None,
                      suffix: str = 'png', dpi: int = 320) -> typing.List[str]:
        """pdf转图片"""
        return ConvertPdf.pdf_to_images(str(pdf_path), save_path, suffix, dpi)

    @staticmethod
    def split_pdf(pdf_profile: PdfProfile, *split_words: str) -> typing.List[TableProfile]:
        """分割pdf"""
        return ProcessPdfProfile.split_pdf(pdf_profile, *split_words)

    @staticmethod
    def split_pdf_image(profile: TableProfile, image: numpy.ndarray, zoom: float = 2):
        """切割pdf图片"""
        ProcessPdfProfile.split_pdf_image(profile, image, zoom)
