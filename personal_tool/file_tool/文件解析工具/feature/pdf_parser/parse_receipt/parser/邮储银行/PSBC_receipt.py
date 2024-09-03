from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.PSBC_receipt_type import PSBCReceiptType
from ...entity.receipt_parser import ReceiptParser


class PSBCReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("邮储银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if self._judge_images(0.1):
            return True
        return False

    def parse(self):
        """解析"""
        for pdf_profile in self.pdf_profiles:
            for receipt_profile in PdfUtil.split_receipt_pdf(pdf_profile):
                self._parse_receipt(receipt_profile, PSBCReceiptType)
