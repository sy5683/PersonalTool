import abc
import os
import time
import typing
from pathlib import Path

import cv2
import numpy

from ..process_opencv_image import ProcessOpenCVImage
from ..screenshot.screenshot import Screenshot


class MatchImage:

    @classmethod
    def get_image_pos(cls, image: typing.Union[numpy.ndarray, Path, str], **kwargs) -> typing.Tuple[int, int]:
        """获取图片坐标"""
        name = kwargs.get("name", "" if isinstance(image, numpy.ndarray) else Path(image).stem)
        similarity = kwargs.get("similarity", 0.6)
        wait_seconds = kwargs.get("wait_seconds", 120)
        # 1) 处理模板图片
        if isinstance(image, (Path, str)):
            image = ProcessOpenCVImage.read_image(str(image))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        for _ in range(wait_seconds):
            # 2) 获取指定句柄图片或桌面图片
            for window_image in cls._get_window_images(**kwargs):
                window_image = cv2.cvtColor(window_image, cv2.COLOR_BGR2RGB)
                # 3) 匹配图片获取坐标
                # 使用标准相关系数匹配,1表示完美匹配,-1表示糟糕的匹配,0表示没有任何相关性
                result = cv2.matchTemplate(window_image, image, cv2.TM_CCOEFF_NORMED)
                # 使用函数minMaxLoc,确定匹配结果矩阵的最大值和最小值(val)，以及它们的位置(loc)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                if max_val > similarity:
                    x, y = max_loc[:2]
                    # 根据模板图片长宽计算出中心坐标
                    height, width = image.shape[:2]
                    return x + width // 2, y + height // 2
            time.sleep(1)
        raise Exception(f"无法匹配到模板: {name}")

    @classmethod
    @abc.abstractmethod
    def _get_window_rect(cls, handle: int) -> typing.Tuple[int, int, int, int]:
        """获取窗口坐标"""
        return cls.__get_subclass()._get_window_rect(handle)

    @classmethod
    def _get_window_images(cls, **kwargs) -> typing.List[numpy.ndarray]:
        """获取窗口图片"""
        handle = kwargs.get("handle")
        cut_item = kwargs.get("cut_item", ((0, 0), (1, 1)))
        images = []
        # 1) 获取桌面图片
        for image in Screenshot.get_screenshot_images():
            # 2) 如果需要获取窗口图片，则获取窗口坐标，再从桌面图片中截取
            if handle:
                left, top, right, bottom = cls._get_window_rect(handle)
                image = image[top:bottom, left:right]
            # 3) 有时为了出现多个定位时的准确度，需要对图片进行裁剪
            if cut_item != ((0, 0), (1, 1)):
                image = cls.__cut_image(image, cut_item)
            images.append(image)
        return images

    @staticmethod
    def __cut_image(image: numpy.ndarray,
                    cut_item: typing.Tuple[typing.Tuple[int, int], typing.Tuple[int, int]]) -> numpy.ndarray:
        """裁剪图片"""
        height, width = image.shape[:2]
        left = int(width * cut_item[0][0])
        top = int(height * cut_item[0][1])
        right = int(width * (1 - cut_item[1][0]))
        bottom = int(height * (1 - cut_item[1][1]))
        return image[top:bottom, left:right]

    @staticmethod
    def __get_subclass():
        if os.name == "nt":
            from .match_image_windows import MatchImageWindows
            return MatchImageWindows
        elif os.name == "posix":
            from .match_image_linux import MatchImageLinux
            return MatchImageLinux
        raise Exception(f"未知的操作系统类型: {os.name}")
