import os
import typing

from common_util.file_util.file_util.file_util import FileUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil
from common_util.file_util.zip_util.zip_util import ZipUtil


class CompressFeature:

    @staticmethod
    def compress_pdf_size(pdf_paths: typing.Tuple[str, ...], dpi: int):
        """压缩pdf大小"""
        for pdf_path in pdf_paths:
            image_paths = PdfUtil.pdf_to_images(pdf_path, dpi=dpi)
            pdf_path = PdfUtil.images_to_pdf(image_paths)
            for image_path in image_paths:
                os.remove(image_path)
            FileUtil.open_file(pdf_path)

    @staticmethod
    def decompress(file_paths: typing.Tuple[str, ...], password: str = None):
        """解压"""
        for file_path in file_paths:
            save_paths = ZipUtil.decompress(file_path, password)
            FileUtil.open_file(next(save_paths))
