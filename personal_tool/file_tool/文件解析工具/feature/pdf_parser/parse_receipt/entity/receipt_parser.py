import abc
import sys
import typing
from pathlib import Path

import cv2
import numpy

from common_util.file_util.file_util.file_util import FileUtil
from common_util.file_util.image_util.image_util import ImageUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil
from common_util.file_util.pdf_util.pdf_utils.entity.pdf_profile import ReceiptProfile
from .receipt import Receipt


class ReceiptParser(metaclass=abc.ABCMeta):

    def __init__(self, bank_name: str, receipt_path: str, **kwargs):
        self.bank_name = bank_name  # 银行名称
        self.receipt_path = receipt_path  # 回单路径
        self.pdf_profiles = PdfUtil.get_pdf_profiles(receipt_path)
        self.receipts: typing.List[Receipt] = []

    @abc.abstractmethod
    def judge(self) -> bool:
        """判断是否为当前格式"""

    @abc.abstractmethod
    def parse_receipt(self):
        """解析回单"""

    def _judge_images(self, *image_names: str, different: float):
        """比较图片"""
        judge_images = self.__get_judge_images(*image_names)
        for image in PdfUtil.get_pdf_images(self.receipt_path):
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            elif len(image.shape) == 3 and image.shape[2] != 3:
                continue
            for judge_image in judge_images:
                if self.__compare_image(image, judge_image) < different:
                    return True
                image = cv2.flip(image, 0)  # 垂直翻转图片
                if self.__compare_image(image, judge_image) < different:
                    return True
        return False

    def _parse_receipt(self, receipt_profile: ReceiptProfile, receipt_type_class):
        receipt_types = []
        for receipt_type_class in receipt_type_class.__subclasses__():
            receipt_type = receipt_type_class(receipt_profile)
            if receipt_type.judge():
                receipt_types.append(receipt_type)
        if not len(receipt_types):
            raise ValueError(f"{self.bank_name}回单pdf中有无法解析的回单")
        elif len(receipt_types) > 1:
            raise ValueError(f"{self.bank_name}回单pdf中有匹配多个格式的回单")
        else:
            self.receipts.append(receipt_types[0].get_receipt())

    @staticmethod
    def __compare_image(image: numpy.ndarray, judge_image: numpy.ndarray) -> float:
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

    def __get_judge_images(self, *image_names: str) -> typing.List[numpy.ndarray]:
        """获取判断图片"""
        image_dir_path = Path(sys.modules[self.__module__].__file__).parent.joinpath("judge_image")
        FileUtil.make_dir(image_dir_path)
        judge_images = []
        for image_name in image_names:
            image_path = image_dir_path.joinpath(image_name)
            assert image_path.exists(), f"判断图片不存在: {image_name}"
            judge_images.append(ImageUtil.read_opencv_image(image_path))
        return judge_images
