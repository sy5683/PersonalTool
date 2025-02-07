from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.YNRCC_receipt_type import YNRCCReceiptType
from ...entity.receipt_parser import ReceiptParser


class YNRCCReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("云南农村信用社", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        # YNRCC_receipt_type_02格式中的章，会出现被切割成几段的情况，因此这里加一种方式判断
        if self._check_contains("云南农信网上银行电子回单"):  # 放在比较图片之前，可以有效提升判断速度
            return True
        if self._judge_images(0.2):
            return True
        return False

    def parse(self):
        """解析"""
        for pdf_profile in self.pdf_profiles:
            for profile in PdfUtil.split_pdf(pdf_profile):
                self._parse_receipt(profile, YNRCCReceiptType)
        # 解析完成后对整张解析后的银行回单做收支类型等信息的提前和整合
        self._format_parser()
