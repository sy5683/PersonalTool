import abc
import os
import tempfile
import typing
from pathlib import Path

import cv2
import numpy
from PIL import ImageGrab

from ..process_opencv_image import ProcessOpenCVImage


class Screenshot:

    @classmethod
    def screenshot(cls, save_path: typing.Union[Path, str]) -> typing.List[str]:
        """截图"""
        save_paths = []
        save_path, suffix = os.path.splitext(tempfile.mktemp(".jpg") if save_path is None else str(save_path))
        for index, image in enumerate(cls.get_screenshot_images()):
            _save_path = (save_path + f"_{index}" if index else save_path) + suffix
            ProcessOpenCVImage.save_image(image, _save_path)
            save_paths.append(_save_path)
        return save_paths

    @classmethod
    @abc.abstractmethod
    def get_screenshot_images(cls) -> typing.List[numpy.ndarray]:
        """获取截图图片"""
        return cls.__get_subclass().get_screenshot_images()

    @staticmethod
    def _get_pil_screenshot_images() -> typing.List[numpy.ndarray]:
        """获取pil的截图图片"""
        image = ImageGrab.grab()
        try:
            return [cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)]
        finally:
            image.close()

    @staticmethod
    def __get_subclass():
        if os.name == "nt":
            from .screenshot_windows import ScreenshotWindows
            return ScreenshotWindows
        elif os.name == 'posix':
            from .screenshot_linux import ScreenshotLinux
            return ScreenshotLinux
        raise Exception(f"未知的操作系统类型: {os.name}")
