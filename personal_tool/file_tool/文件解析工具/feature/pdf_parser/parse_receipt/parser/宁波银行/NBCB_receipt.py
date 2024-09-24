from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.NBCB_receipt_type import NBCBReceiptType
from ...entity.receipt_parser import ReceiptParser


class NBCBReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("宁波银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if not self._judge_images(0.1):
            return False
        return self._check_contains("宁波银行客户回单")

    def parse(self):
        """解析"""
        for pdf_profile in self.pdf_profiles:
            for receipt_profile in PdfUtil.split_pdf(pdf_profile, "宁波银行客户回单"):
                self._parse_receipt(receipt_profile, NBCBReceiptType)
