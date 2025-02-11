from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.ABC_receipt_type import ABCReceiptType
from ...entity.receipt_parser import ReceiptParser


class ABCReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("农业银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if not self._judge_images(0.4, 0):
            return False
        return self._check_contains("网上银行电子回单")

    def parse(self):
        """解析"""
        for pdf_profile in self.pdf_profiles:
            for profile in PdfUtil.split_pdf(pdf_profile):
                self._parse_receipt(profile, ABCReceiptType)
        # 解析完成后对整张解析后的银行回单做收支类型等信息的提前和整合
        self._format_parser()
