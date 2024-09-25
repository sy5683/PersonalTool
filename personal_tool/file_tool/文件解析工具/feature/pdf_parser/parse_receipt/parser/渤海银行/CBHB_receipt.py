from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.CBHB_receipt_type import CBHBReceiptType
from ...entity.receipt_parser import ReceiptParser


class CBHBReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("渤海银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        return self._check_contains("渤海银行电子印图案")

    def parse(self):
        """解析"""
        for pdf_profile in self.pdf_profiles:
            for profile in PdfUtil.split_pdf(pdf_profile):
                self._parse_receipt(profile, CBHBReceiptType)
