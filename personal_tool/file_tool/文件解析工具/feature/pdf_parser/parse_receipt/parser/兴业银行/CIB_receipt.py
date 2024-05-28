import fitz

from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.CIB_receipt_type import CIBReceiptType
from ...entity.receipt_parser import ReceiptParser


class CIBReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("兴业银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        with fitz.open(self.receipt_path) as pdf:
            if "兴业银行网上回单" in pdf[0].get_text().replace(chr(0xa0), ''):
                return True
            if "www.cib.com.cn" in pdf[0].get_text():
                return True
        return False

    def parse_receipt(self):
        """解析回单"""
        for pdf_profile in self.pdf_profiles:
            for receipt_profile in PdfUtil.split_receipt_pdf(pdf_profile):
                self._parse_receipt(receipt_profile, CIBReceiptType)
