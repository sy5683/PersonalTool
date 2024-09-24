import abc
import re
import typing

from common_util.file_util.pdf_util.pdf_util import PdfUtil
from common_util.file_util.pdf_util.pdf_utils.entity.pdf_element import Cell
from common_util.file_util.pdf_util.pdf_utils.entity.pdf_profile import ReceiptProfile
from .receipt import Receipt


class ReceiptType(metaclass=abc.ABCMeta):

    def __init__(self, bank_name: str, receipt_profile: ReceiptProfile):
        self.bank_name = bank_name
        self.table = receipt_profile.table
        self.words = receipt_profile.words

    def __str__(self):
        types = re.search(r"\d+", self.__class__.__name__).group()
        return f"{self.bank_name}_{types}"

    @abc.abstractmethod
    def judge(self) -> bool:
        """判断是否为当前格式"""

    @abc.abstractmethod
    def get_receipt(self) -> Receipt:
        """解析"""

    @staticmethod
    def _get_account(value: str) -> str:
        return re.sub("账号|[:：]|[|]|基本户", "", value)

    @staticmethod
    def _get_bank(value: str) -> str:
        return re.sub("开户行|[:：]", "", value)

    def _get_cell_relative(self, pattern: str, relative: int = 1) -> Cell:
        """
        根据相对坐标获取单元格的值，主要是用于上侧单元格行数不确定的情况
        只用于左侧单元格是键，右侧单元格是值的情况，relative用于右侧偏移单元格数量
        """
        return self.table.get_cell_relative(pattern, relative)

    @staticmethod
    def _get_name(value: str) -> str:
        return re.sub("全称|户名|[:：]|付款账户名称|收款账户名称", "", value)

    def _get_word(self, pattern: str) -> typing.Union[str, None]:
        return PdfUtil.filter_word(self.words, pattern)

    def _get_words(self, pattern: str) -> typing.List[str]:
        return PdfUtil.filter_words(self.words, pattern)
