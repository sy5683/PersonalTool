import os
import re
import typing
from pathlib import Path

import cv2
import numpy


class ProcessOpenCVImage:
    """处理opencv图片"""

    @classmethod
    def convert_to_jpg(cls, image_path: str, save_path: typing.Union[Path, str]) -> str:
        """转换为jpg图片"""
        image = cls._read_image(image_path)
        if image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        save_path = f"{os.path.splitext(image_path)[0]}.jpg" if save_path is None else str(save_path)
        cls.save_image(image, save_path)
        return save_path

    @classmethod
    def remove_border(cls, image_path: str, color: typing.Union[int, typing.Tuple[int, int, int]],
                      save_path: typing.Union[Path, str]) -> str:
        """去除边框"""
        image = cls._read_image(image_path)
        if isinstance(color, int):
            edges_y, edges_x, _ = numpy.where(image != color)
        else:
            # 如果是单色，可以使用灰度图处理，时间复杂度会快一些
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges_y, edges_x = numpy.where(gray_image != color)
        image = image[min(edges_y):max(edges_y), min(edges_x):max(edges_x)]
        save_path = image_path if save_path is None else str(save_path)
        cls.save_image(image, save_path)
        return save_path

    @staticmethod
    def rotate_image(image: numpy.ndarray, angle: int, times: int) -> numpy.ndarray:
        """图片旋转"""
        height, width = image.shape[:2]
        new_height = int(width * numpy.fabs(numpy.sin(numpy.radians(angle))) +
                         height * numpy.fabs(numpy.cos(numpy.radians(angle))))
        new_width = int(height * numpy.fabs(numpy.sin(numpy.radians(angle))) +
                        width * numpy.fabs(numpy.cos(numpy.radians(angle))))
        rotate_image = cv2.getRotationMatrix2D((width // 2, height // 2), angle * times, 1)
        rotate_image[0, 2] += (new_width - width) // 2
        rotate_image[1, 2] += (new_height - height) // 2
        return cv2.warpAffine(image, rotate_image, (new_width, new_height))

    @classmethod
    def save_image(cls, image: numpy.ndarray, image_path: str):
        """保存图片"""
        if cls._check_path_is_chinese(image_path):
            cv2.imencode(Path(image_path).suffix, image)[1].tofile(image_path)
        else:
            cv2.imwrite(image_path, image)

    @staticmethod
    def _check_path_is_chinese(path: str) -> bool:
        """判断路径中是否有中文，opencv读取保存中文路径图片时需要特殊处理"""
        return True if re.search(r"[\u4e00-\u9fa5]+", path) else False

    @classmethod
    def _read_image(cls, image_path: str) -> numpy.ndarray:
        """读取图片"""
        if cls._check_path_is_chinese(image_path):
            return cv2.imdecode(numpy.fromfile(image_path, dtype=numpy.uint8), cv2.IMREAD_COLOR)
        else:
            return cv2.imread(image_path)
