import abc
import typing

from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt import Receipt


class ReceiptProfile(metaclass=abc.ABCMeta):

    def __init__(self, bank_name: str, receipt_path: str, **kwargs):
        self.bank_name = bank_name  # 银行名称
        self.receipt_path = receipt_path  # 回单路径
        self.pdf_profiles = PdfUtil.get_pdf_profiles(receipt_path)
        self.receipts: typing.List[Receipt] = []

    @abc.abstractmethod
    def judge(self) -> bool:
        """判断是否为当前格式"""

    @abc.abstractmethod
    def parse_receipt(self):
        """解析回单"""
