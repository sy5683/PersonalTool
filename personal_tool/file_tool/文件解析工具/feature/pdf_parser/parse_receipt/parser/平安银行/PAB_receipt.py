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
            for profile in PdfUtil.split_pdf(pdf_profile, "bank.pingan.com"):
                self._parse_receipt(profile, PABReceiptType)
        # 解析完成后对整张解析后的银行回单做收支类型等信息的提前和整合
        self._format_parser()
