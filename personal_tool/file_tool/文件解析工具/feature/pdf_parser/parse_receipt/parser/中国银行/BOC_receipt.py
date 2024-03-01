import cv2

from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.BOC_receipt_type import BOCReceiptType
from ...entity.receipt_parser import ReceiptParser


class BOCReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("中国银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if not self.__judge_images("BOC_image_01.png", different=0.2):
            return False
        return True

    def parse_receipt(self):
        """解析回单"""
        for pdf_profile in self.pdf_profiles:
            for receipt_profile in PdfUtil.split_receipt_pdf(pdf_profile):
                self._parse_receipt(receipt_profile, BOCReceiptType)

    def __judge_images(self, *image_names: str, different: float):
        """比较图片"""
        judge_images = self._get_judge_images(*image_names)
        for image in PdfUtil.get_pdf_images(self.receipt_path):
            if image is None:
                continue
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            elif len(image.shape) == 3 and image.shape[2] != 3:
                continue
            for judge_image in judge_images:
                if self._compare_image(image, judge_image) < different:
                    return True
        return False
