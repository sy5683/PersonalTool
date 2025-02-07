from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.ICBC_receipt_type import ICBCReceiptType
from ...entity.receipt_parser import ReceiptParser


class ICBCReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        kwargs['threshold_x'] = 25
        super().__init__("工商银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        return self._check_contains("中国工商银行电子化回单", "www.icbc.com.cn")

    def parse(self):
        """解析"""
        for pdf_profile in self.pdf_profiles:
            for profile in PdfUtil.split_pdf(pdf_profile):
                if not profile.table and len(profile.words) < 6:
                    continue
                self._parse_receipt(profile, ICBCReceiptType)
        # 解析完成后对整张解析后的银行回单做收支类型等信息的提前和整合
        self._format_parser()
