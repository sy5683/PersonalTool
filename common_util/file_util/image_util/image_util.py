import pathlib
import typing

import numpy

from .image_utils.match_image.match_image import MatchImage
from .image_utils.process_opencv_image import ProcessOpenCVImage
from .image_utils.process_pil_image import ProcessPILImage
from .image_utils.screenshot.screenshot import Screenshot


class ImageUtil:

    @staticmethod
    def compare_image(image: numpy.ndarray, judge_image: numpy.ndarray) -> float:
        """对比两张图片的相似度"""
        return ProcessOpenCVImage.compare_image(image, judge_image)

    @staticmethod
    def convert_to_jpg_by_opencv(image_path: typing.Union[pathlib.Path, str],
                                 save_path: typing.Union[pathlib.Path, str] = None) -> str:
        """通过opencv将图片转换为jpg图片"""
        return ProcessOpenCVImage.convert_to_jpg(str(image_path), save_path)

    @staticmethod
    def convert_to_jpg_by_pil(image_path: typing.Union[pathlib.Path, str],
                              save_path: typing.Union[pathlib.Path, str] = None) -> str:
        """通过pil将图片转换为jpg图片"""
        return ProcessPILImage.convert_to_jpg(str(image_path), save_path)

    @staticmethod
    def get_image_pos(image: typing.Union[numpy.ndarray, pathlib.Path, str], **kwargs) -> typing.Tuple[int, int]:
        """获取图片坐标"""
        return MatchImage.get_image_pos(image, **kwargs)

    @staticmethod
    def image_to_transparent(image: numpy.ndarray, mask_image: numpy.ndarray) -> numpy.ndarray:
        """根据蒙版将图片透明化"""
        return ProcessOpenCVImage.image_to_transparent(image, mask_image)

    @staticmethod
    def re_scale(image_path: typing.Union[pathlib.Path, str], new_size: typing.Tuple[int, int],
                 save_path: typing.Union[pathlib.Path, str] = None, resize: bool = False) -> str:
        """转换图片比例"""
        return ProcessPILImage.re_scale(str(image_path), new_size, save_path, resize)

    @staticmethod
    def read_opencv_image(image_path: typing.Union[pathlib.Path, str]) -> numpy.ndarray:
        """读取图片"""
        return ProcessOpenCVImage.read_image(str(image_path))

    @staticmethod
    def remove_border(image: numpy.ndarray,
                      color: typing.Union[int, typing.Tuple[int, int, int]] = 255) -> numpy.ndarray:
        """去除边框"""
        return ProcessOpenCVImage.remove_border(image, color)

    @staticmethod
    def rotate_image(image: numpy.ndarray, angle: int, times: int = 1) -> numpy.ndarray:
        """图片旋转"""
        return ProcessOpenCVImage.rotate_image(image, angle, times)

    @staticmethod
    def save_opencv_image(image: numpy.ndarray, image_path: typing.Union[pathlib.Path, str]):
        """保存opencv图片"""
        ProcessOpenCVImage.save_image(image, str(image_path))

    @staticmethod
    def screenshot(save_path: typing.Union[pathlib.Path, str] = None) -> typing.List[str]:
        """截图"""
        return Screenshot.screenshot(save_path)
