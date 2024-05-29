from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.CDB_receipt_type import CDBReceiptType
from ...entity.receipt_parser import ReceiptParser


class CDBReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("国家开发银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        return self._check_contains("国家开发银行")

    def parse_receipt(self):
        """解析回单"""
        for pdf_profile in self.pdf_profiles:
            for receipt_profile in PdfUtil.split_receipt_pdf(pdf_profile, "国家开发银行电子回单"):
                self._parse_receipt(receipt_profile, CDBReceiptType)
