import abc
import re
import sys
import typing
from pathlib import Path

import cv2
import fitz
import numpy

from common_util.file_util.file_util.file_util import FileUtil
from common_util.file_util.image_util.image_util import ImageUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil


class PdfParserBase(metaclass=abc.ABCMeta):

    def __init__(self, parser_type: str, pdf_path: str, **kwargs):
        self.parser_type = parser_type  # 解析器类型
        self.pdf_path = pdf_path  # 文件路径
        self.pdf_profiles = PdfUtil.get_pdf_profiles(pdf_path, kwargs.get("threshold_x", 10))

    @abc.abstractmethod
    def judge(self) -> bool:
        """判断是否为当前格式"""

    @abc.abstractmethod
    def parse(self):
        """解析"""

    def _check_contains(self, *values: str) -> bool:
        """判断pdf中是否包含"""
        with fitz.open(self.pdf_path) as pdf:
            pdf_text = re.sub(r"\s+", "", pdf[0].get_text())
            for value in values:
                if value in pdf_text:
                    return True
        return False

    def _get_judge_images(self) -> typing.List[numpy.ndarray]:
        """获取判断图片"""
        image_dir_path = Path(sys.modules[self.__module__].__file__).parent.joinpath("judge_image")
        FileUtil.make_dir(image_dir_path)
        judge_images = [ImageUtil.read_opencv_image(image_path) for image_path in image_dir_path.rglob("*.*")]
        if not judge_images:
            raise FileNotFoundError("缺少判断图片")
        return judge_images

    def _judge_images(self, different: float):
        """比较图片"""
        judge_images = self._get_judge_images()
        for index, image in enumerate(PdfUtil.get_pdf_images(self.pdf_path)):
            if image is None:
                continue
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            if image.shape[2] == 4:
                image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
            # ImageUtil.save_opencv_image(image, f"D:\\{index}.png")
            for judge_image in judge_images:
                if ImageUtil.compare_image(image, judge_image) < different:
                    return True
                # 颜色反转
                if image.shape[2] == 3:
                    reverse_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    if ImageUtil.compare_image(reverse_image, judge_image) < different:
                        return True
        return False
