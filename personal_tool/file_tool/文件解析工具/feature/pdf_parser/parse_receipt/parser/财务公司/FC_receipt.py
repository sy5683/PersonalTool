from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.FC_receipt_type import FCReceiptType
from ...entity.receipt_parser import ReceiptParser


class FCReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("财务公司", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if not self._judge_images("FC_image_01.png", different=0.3):
            return False
        return True

    def parse_receipt(self):
        """解析回单"""
        for pdf_profile in self.pdf_profiles:
            for receipt_profile in PdfUtil.split_receipt_pdf(pdf_profile):
                self._parse_receipt(receipt_profile, FCReceiptType)
