from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.PAB_receipt_type import PABReceiptType
from ...entity.receipt_parser import ReceiptParser


class PABReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("平安银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        return self._check_contains("bank.pingan.com")

    def parse(self):
        """解析"""
        for pdf_profile in self.pdf_profiles:
            for receipt_profile in PdfUtil.split_receipt_pdf(pdf_profile, "bank.pingan.com"):
                self._parse_receipt(receipt_profile, PABReceiptType)
