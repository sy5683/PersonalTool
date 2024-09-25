from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.BOCOM_receipt_type import BOCOMReceiptType
from ...entity.receipt_parser import ReceiptParser


class BOCOMReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("交通银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        return self._judge_images(0.2)

    def parse(self):
        """解析"""
        for pdf_profile in self.pdf_profiles:
            for profile in PdfUtil.split_pdf(pdf_profile):
                self._parse_receipt(profile, BOCOMReceiptType)
