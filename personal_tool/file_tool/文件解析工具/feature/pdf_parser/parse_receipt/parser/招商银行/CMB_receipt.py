import cv2

from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.CMB_receipt_type import CMBReceiptType
from ...entity.receipt_parser import ReceiptParser


class CMBReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("招商银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if not self.__judge_images("CMB_image_01.png", different=0.3):
            return False
        return True

    def parse_receipt(self):
        """解析回单"""
        for pdf_profile in self.pdf_profiles:
            for receipt_profile in PdfUtil.split_receipt_pdf(pdf_profile):
                self._parse_receipt(receipt_profile, CMBReceiptType)

    def __judge_images(self, *image_names: str, different: float):
        """比较图片"""
        judge_images = self._get_judge_images(*image_names)
        for image in PdfUtil.get_pdf_images(self.receipt_path):
            if image is None:
                continue
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            elif len(image.shape) == 3 and image.shape[2] not in (3, 4):
                continue
            if image.shape[2] == 4:
                image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
            elif image.shape[2] == 3:
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            for judge_image in judge_images:
                if self._compare_image(image, judge_image) < different:
                    return True
                image = cv2.flip(image, 0)  # 垂直翻转图片
                if self._compare_image(image, judge_image) < different:
                    return True
        return False
