import typing
from pathlib import Path

from .pdf_utils.convert_pdf import ConvertPdf
from .pdf_utils.entity.pdf_element import Table, Word
from .pdf_utils.entity.pdf_profile import PdfProfile
from .pdf_utils.parser_pdf import ParserPdf


class PdfUtil:

    @staticmethod
    def get_pdf_profiles(pdf_path: typing.Union[Path, str], threshold_x: int) -> typing.List[PdfProfile]:
        """获取pdf内容"""
        return ParserPdf.get_pdf_profiles(str(pdf_path), threshold_x)

    @staticmethod
    def get_pdf_tables(pdf_path: typing.Union[Path, str]) -> typing.List[Table]:
        """获取pdf中的表格"""
        return ParserPdf.get_pdf_tables(str(pdf_path))

    @staticmethod
    def get_pdf_words(pdf_path: typing.Union[Path, str], threshold_x: int = 10) -> typing.List[Word]:
        """获取pdf中的文字"""
        return ParserPdf.get_pdf_words(str(pdf_path), threshold_x)

    @staticmethod
    def pdf_to_images(pdf_path: typing.Union[Path, str], save_path: typing.Union[Path, str] = None,
                      suffix: str = 'png') -> typing.List[str]:
        """pdf转图片"""
        return ConvertPdf.pdf_to_images(str(pdf_path), save_path, suffix)

    @staticmethod
    def images_to_pdf(image_paths: typing.List[typing.Union[Path, str]],
                      save_path: typing.Union[Path, str] = None) -> str:
        """图片转pdf"""
        return ConvertPdf.images_to_pdf([str(image_path) for image_path in image_paths], save_path)
