import abc
import logging
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
from common_util.file_util.pdf_util.pdf_utils.entity.pdf_profile import ReceiptProfile
from .receipt import Receipt
from ...base.pdf_parser_base import PdfParserBase


class ReceiptParser(PdfParserBase, metaclass=abc.ABCMeta):
    parser_name = "银行回单"

    def __init__(self, bank_name: str, receipt_path: str, **kwargs):
        super().__init__(bank_name, receipt_path)  # 银行名称
        self.receipt_path = receipt_path  # 回单路径
        self.receipts: typing.List[Receipt] = []

    def _check_contains(self, *values: str) -> bool:
        """判断pdf中是否包含"""
        with fitz.open(self.receipt_path) as pdf:
            pdf_text = re.sub(r"\s+", "", pdf[0].get_text())
            for value in values:
                if value in pdf_text:
                    return True
        return False

    @staticmethod
    def _compare_image(image: numpy.ndarray, judge_image: numpy.ndarray) -> float:
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
        compare = numpy.sum(cv2.absdiff(image, judge_image)) / 255 / width / height
        return compare

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
        for index, image in enumerate(PdfUtil.get_pdf_images(self.receipt_path)):
            if image is None:
                continue
            # ImageUtil.save_opencv_image(image, f"E:\\Download\\{index}.png")
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            if image.shape[2] == 4:
                image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
            for judge_image in judge_images:
                if self._compare_image(image, judge_image) < different:
                    return True
                # 颜色反转
                if image.shape[2] == 3:
                    reverse_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    if self._compare_image(reverse_image, judge_image) < different:
                        return True
        return False

    def _parse_receipt(self, receipt_profile: ReceiptProfile, receipt_type_class):
        """解析"""
        if not receipt_profile.table and not receipt_profile.words:
            return   # 跳过没有表格和文本的页
        receipt_types = []
        for receipt_type_class in receipt_type_class.__subclasses__():
            receipt_type = receipt_type_class(receipt_profile)
            # noinspection PyBroadException
            try:
                if receipt_type.judge():
                    receipt_types.append(receipt_type)
            except Exception:
                pass
        if not len(receipt_types):
            logging.error(f"{self.parser_type}回单pdf中有无法解析的回单: {receipt_profile.words[0].text}")
            raise ValueError(f"{self.parser_type}回单pdf中有无法解析的回单")
        elif len(receipt_types) > 1:
            logging.error(f"{self.parser_type}回单pdf中有匹配多个格式的回单: {receipt_types}")
            raise ValueError(f"{self.parser_type}回单pdf中有匹配多个格式的回单")
        else:
            receipt = receipt_types[0].get_receipt()
            if receipt:
                self.receipts.append(receipt)
