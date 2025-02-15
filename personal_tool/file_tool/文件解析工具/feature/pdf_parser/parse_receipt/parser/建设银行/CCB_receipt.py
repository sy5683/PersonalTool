from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.CCB_receipt_type import CCBReceiptType
from ...entity.receipt_parser import ReceiptParser


class ICBCReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("建设银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if self._check_contains("中国建设银行网上银行电子回执", "中国建设银行单位客户专用回单"):
            return True
        if self._judge_images(0.05, 0):
            return True
        return False

    def parse(self):
        """解析"""
        for pdf_profile in self.pdf_profiles:
            for profile in PdfUtil.split_pdf(pdf_profile):
                self._parse_receipt(profile, CCBReceiptType)
        # 解析完成后对整张解析后的银行回单做收支类型等信息的提前和整合
        self._format_parser()
