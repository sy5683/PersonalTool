import typing
from pathlib import Path

from .pdf_utils.convert_pdf import ConvertPdf


class PdfUtil:

    @staticmethod
    def pdf_to_images(pdf_path: typing.Union[Path, str], suffix: str = 'png') -> typing.List[str]:
        """pdf转图片"""
        return ConvertPdf.pdf_to_images(str(pdf_path), suffix)

    @staticmethod
    def images_to_pdf(image_paths: typing.List[typing.Union[Path, str]], pdf_path: typing.Union[Path, str]) -> str:
        """图片转pdf"""
        return ConvertPdf.images_to_pdf(image_paths, str(pdf_path))
