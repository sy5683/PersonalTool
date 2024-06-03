from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.ICBC_receipt_type import ICBCReceiptType
from ...entity.receipt_parser import ReceiptParser


class ICBCReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("工商银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        return self._check_contains("中国工商银行电子化回单", "www.icbc.com.cn")

    def parse(self):
        """解析"""
        for pdf_profile in self.pdf_profiles:
            for receipt_profile in PdfUtil.split_receipt_pdf(pdf_profile):
                if not receipt_profile.table and len(receipt_profile.words) < 6:
                    continue
                self._parse_receipt(receipt_profile, ICBCReceiptType)
