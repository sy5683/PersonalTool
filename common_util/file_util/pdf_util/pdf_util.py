import typing
from pathlib import Path

from common_core.base.util_base import UtilBase
from .pdf_utils.convert_pdf import ConvertPdf


class PdfUtil(UtilBase):

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
