import fitz

from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.CEXIM_receipt_type import CEXIMReceiptType
from ...entity.receipt_parser import ReceiptParser


class CEXIMReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("中国进出口银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        with fitz.open(self.receipt_path) as pdf:
            if "中国进出口银行单位客户专用回单" not in pdf[0].get_text():
                return False
        return True

    def parse_receipt(self):
        """解析回单"""
        for pdf_profile in self.pdf_profiles:
            for receipt_profile in PdfUtil.split_receipt_pdf(pdf_profile):
                self._parse_receipt(receipt_profile, CEXIMReceiptType)
