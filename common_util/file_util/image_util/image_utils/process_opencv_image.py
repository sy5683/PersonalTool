import os
import re
import typing
from pathlib import Path

import cv2
import numpy


class ProcessOpenCVImage:

    @staticmethod
    def compare_image(image: numpy.ndarray, judge_image: numpy.ndarray) -> float:
        """对比两张图片的相似度"""
        # 如果图片为单通道，这将其变为三通道，如果不是单通道或者三通道，说明图片解析失败
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        elif len(image.shape) == 3 and image.shape[2] != 3:
            return 1
        if len(judge_image.shape) == 2:
            judge_image = cv2.cvtColor(judge_image, cv2.COLOR_GRAY2BGR)
        elif len(judge_image.shape) == 3 and judge_image.shape[2] != 3:
            return 1
        height, width = judge_image.shape[:2]
        # 缩放一致大小
        image = cv2.resize(image, (width, height), interpolation=cv2.INTER_NEAREST)
        # 求和每个像素点之间的差异，除以255是为了归一化，之后再求整体差异性
        return numpy.sum(cv2.absdiff(image, judge_image)) / 255 / width / height

    @classmethod
    def convert_to_jpg(cls, image_path: str, save_path: typing.Union[Path, str]) -> str:
        """转换为jpg图片"""
        image = cls.read_image(image_path)
        if image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        save_path = f"{os.path.splitext(image_path)[0]}.jpg" if save_path is None else str(save_path)
        cls.save_image(image, save_path)
        return save_path

    @staticmethod
    def image_to_transparent(image: numpy.ndarray, mask_image: numpy.ndarray) -> numpy.ndarray:
        """根据蒙版将图片透明化"""
        transparent_image = cv2.bitwise_and(image, image, mask=mask_image)
        transparent_image = cv2.cvtColor(transparent_image, cv2.COLOR_RGB2RGBA)
        transparent_image[:, :, 3] = mask_image
        return transparent_image

    @classmethod
    def read_image(cls, image_path: str) -> numpy.ndarray:
        """读取图片"""
        if cls._check_path_is_chinese(image_path):
            return cv2.imdecode(numpy.fromfile(image_path, dtype=numpy.uint8), cv2.IMREAD_COLOR)
        else:
            return cv2.imread(image_path)

    @staticmethod
    def remove_border(image: numpy.ndarray, color: typing.Union[int, typing.Tuple[int, int, int]]) -> numpy.ndarray:
        """去除边框"""
        if isinstance(color, int):
            edges_y, edges_x, _ = numpy.where(image < color)
        else:
            # 如果是单色，可以使用灰度图处理，时间复杂度会快一些
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges_y, edges_x = numpy.where(gray_image < color)
        return image[min(edges_y):max(edges_y), min(edges_x):max(edges_x)]

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
