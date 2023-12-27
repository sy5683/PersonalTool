import typing
from pathlib import Path

from .pdf_utils.convert_pdf import ConvertPdf
from .pdf_utils.entity.pdf_element import Table
from .pdf_utils.parser_pdf import ParserPdf


class PdfUtil:

    @staticmethod
    def get_pdf_tables(pdf_path: typing.Union[Path, str]) -> typing.List[Table]:
        """获取pdf中的表格"""
        return ParserPdf.get_pdf_tables(str(pdf_path))

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
