import abc

from common_util.file_util.pdf_util.pdf_utils.entity.pdf_profile import ReceiptProfile
from ....entity.receipt import Receipt


class ICBCReceiptType(metaclass=abc.ABCMeta):

    def __init__(self, receipt_profile: ReceiptProfile):
        self.table = receipt_profile.table
        self.words = receipt_profile.words

    @abc.abstractmethod
    def judge(self) -> bool:
        """判断是否为当前格式"""

    @abc.abstractmethod
    def get_receipt(self) -> Receipt:
        """解析回单"""
