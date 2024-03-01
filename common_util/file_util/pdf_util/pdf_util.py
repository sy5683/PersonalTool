import typing
from pathlib import Path

import numpy

from .pdf_utils.convert_pdf import ConvertPdf
from .pdf_utils.entity.pdf_element import Table, Word
from .pdf_utils.entity.pdf_profile import PdfProfile, ReceiptProfile
from .pdf_utils.extract_pdf import ExtractPdf
from .pdf_utils.parse_pdf import ParsePdf
from .pdf_utils.process_pdf_profile import ProcessPdfProfile


class PdfUtil:

    @staticmethod
    def get_pdf_images(pdf_path: str) -> typing.List[numpy.ndarray]:
        """提取pdf中图片"""
        return ExtractPdf.get_pdf_images(pdf_path)

    @staticmethod
    def get_pdf_profiles(pdf_path: typing.Union[Path, str], threshold_x: int = 10) -> typing.List[PdfProfile]:
        """获取pdf内容"""
        return ParsePdf.get_pdf_profiles(str(pdf_path), threshold_x)

    @staticmethod
    def get_pdf_tables(pdf_path: typing.Union[Path, str]) -> typing.List[Table]:
        """获取pdf中的表格"""
        return ParsePdf.get_pdf_tables(str(pdf_path))

    @staticmethod
    def get_pdf_words(pdf_path: typing.Union[Path, str], threshold_x: int = 10) -> typing.List[Word]:
        """获取pdf中的文字"""
        return ParsePdf.get_pdf_words(str(pdf_path), threshold_x)

    @staticmethod
    def images_to_pdf(image_paths: typing.List[typing.Union[Path, str]],
                      save_path: typing.Union[Path, str] = None) -> str:
        """图片转pdf"""
        return ConvertPdf.images_to_pdf([str(image_path) for image_path in image_paths], save_path)

    @staticmethod
    def merge_words(words: typing.List[Word], threshold: int = 1) -> typing.List[Word]:
        """合并pdf文字"""
        return ProcessPdfProfile.merge_words(words, threshold)

    @staticmethod
    def pdf_to_images(pdf_path: typing.Union[Path, str], save_path: typing.Union[Path, str] = None,
                      suffix: str = 'png') -> typing.List[str]:
        """pdf转图片"""
        return ConvertPdf.pdf_to_images(str(pdf_path), save_path, suffix)

    @staticmethod
    def split_receipt_pdf(pdf_profile: PdfProfile) -> typing.List[ReceiptProfile]:
        """分割回单pdf"""
        return ProcessPdfProfile.split_receipt_pdf(pdf_profile)
