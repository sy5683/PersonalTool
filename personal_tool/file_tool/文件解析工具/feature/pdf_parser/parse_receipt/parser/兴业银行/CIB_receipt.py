from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.CIB_receipt_type import CIBReceiptType
from ...entity.receipt_parser import ReceiptParser


class CIBReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("兴业银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        return self._check_contains("兴业银行网上回单", "www.cib.com.cn")

    def parse(self):
        """解析"""
        for pdf_profile in self.pdf_profiles:
            for profile in PdfUtil.split_pdf(pdf_profile, "仅在打印回单或账单的场景下使用。"):
                self._parse_receipt(profile, CIBReceiptType)
        # 解析完成后对整张解析后的银行回单做收支类型等信息的提前和整合
        self._format_parser()
