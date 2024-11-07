import typing

import numpy

from .screenshot import Screenshot


class ScreenshotLinux(Screenshot):

    @classmethod
    def get_screenshot_images(cls) -> typing.List[numpy.ndarray]:
        """获取截图图片"""
        return cls._get_pil_screenshot_images()
