import abc
import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.file_util.pdf_util.pdf_utils.entity.pdf_profile import ReceiptProfile
from .receipt import Receipt


class ReceiptType(metaclass=abc.ABCMeta):

    def __init__(self, receipt_profile: ReceiptProfile):
        self.table = receipt_profile.table
        self.words = receipt_profile.words

    @abc.abstractmethod
    def judge(self) -> bool:
        """判断是否为当前格式"""

    @abc.abstractmethod
    def get_receipt(self) -> Receipt:
        """解析"""

    @staticmethod
    def _get_account(value: str) -> str:
        return re.sub("账号|[:：]|[|]|基本户", "", value)

    def _get_amount(self, key_index: int, value_index: int) -> float:
        """获取金额"""
        for row in range(self.table.max_rows):
            row_values = self.table.get_row_values(row)
            if re.search(r"^合计金额$", row_values[key_index]):
                return NumberUtil.to_amount(row_values[value_index])
        raise ValueError("格式异常，回单无法提取金额")

    def _get_word(self, pattern: str) -> str:
        for word in self.words:
            if re.search(pattern, word.text):
                return re.findall(pattern, word.text)[0]

    @staticmethod
    def _get_name(value: str) -> str:
        return re.sub("全称|户名|[:：]|付款账户名称|收款账户名称", "", value)
