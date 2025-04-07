from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.CGB_receipt_type import CGBReceiptType
from ...entity.receipt_parser import ReceiptParser


class CGBReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("广发银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        return self._judge_images(0.1, 0)

    def parse(self):
        """解析"""
        for pdf_profile in self.pdf_profiles:
            for profile in PdfUtil.split_pdf(pdf_profile, "广发网上银行电子回单"):
                self._parse_receipt(profile, CGBReceiptType)
        # 解析完成后对整张解析后的银行回单做收支类型等信息的提前和整合
        self._format_parser()
