import typing
from pathlib import Path

import numpy

from .image_utils.process_opencv_image import ProcessOpenCVImage
from .image_utils.process_pil_image import ProcessPILImage


class ImageUtil:

    @staticmethod
    def convert_to_jpg_by_opencv(image_path: typing.Union[Path, str], save_path: typing.Union[Path, str] = None) -> str:
        """通过opencv将图片转换为jpg图片"""
        return ProcessOpenCVImage.convert_to_jpg(str(image_path), save_path)

    @staticmethod
    def convert_to_jpg_by_pil(image_path: typing.Union[Path, str]) -> str:
        """通过pil将图片转换为jpg图片"""
        return ProcessPILImage.convert_to_jpg(str(image_path))

    @staticmethod
    def remove_border(image_path: typing.Union[Path, str], color: typing.Union[int, typing.Tuple[int, int, int]] = 255,
                      save_path: typing.Union[Path, str] = None) -> str:
        """去除边框"""
        return ProcessOpenCVImage.remove_border(str(image_path), color, save_path)

    @staticmethod
    def save_opencv_image(image: numpy.ndarray, image_path: typing.Union[Path, str]):
        """保存opencv图片"""
        ProcessOpenCVImage.save_image(image, str(image_path))

    @staticmethod
    def to_a4_size(image_path: typing.Union[Path, str], save_path: typing.Union[Path, str] = None) -> str:
        """将图片转换为A4比例"""
        return ProcessPILImage.to_a4_size(str(image_path), save_path)
