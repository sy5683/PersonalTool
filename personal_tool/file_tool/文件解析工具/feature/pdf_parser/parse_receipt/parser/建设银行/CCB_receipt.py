import re

import fitz

from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.CCB_receipt_type import CCBReceiptType
from ...entity.receipt_parser import ReceiptParser


class ICBCReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("建设银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        with fitz.open(self.receipt_path) as pdf:
            if not re.search("中国建设银行网上银行电子回执|中国建设银行单位客户专用回单", pdf[0].get_text()):
                return False
        return True

    def parse_receipt(self):
        """解析回单"""
        for pdf_profile in self.pdf_profiles:
            for receipt_profile in PdfUtil.split_receipt_pdf(pdf_profile):
                self._parse_receipt(receipt_profile, CCBReceiptType)
