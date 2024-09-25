import abc
import re
import typing

from common_util.file_util.pdf_util.pdf_util import PdfUtil
from common_util.file_util.pdf_util.pdf_utils.entity.pdf_element import Cell
from common_util.file_util.pdf_util.pdf_utils.entity.pdf_profile import TableProfile
from .invoice import Invoice


class InvoiceType(metaclass=abc.ABCMeta):

    def __init__(self, invoice_name: str, profile: TableProfile):
        self.invoice_name = invoice_name
        self.table = profile.table
        self.words = profile.words

    def __str__(self):
        types = re.search(r"\d+", self.__class__.__name__).group()
        return f"{self.invoice_name}_{types}"

    @abc.abstractmethod
    def judge(self) -> bool:
        """判断是否为当前格式"""

    @abc.abstractmethod
    def get_invoice(self) -> Invoice:
        """解析"""

    def _get_cell_relative(self, pattern: str, relative: int = 1) -> Cell:
        """
        根据相对坐标获取单元格的值，主要是用于上侧单元格行数不确定的情况
        只用于左侧单元格是键，右侧单元格是值的情况，relative用于右侧偏移单元格数量
        """
        return self.table.get_cell_relative(pattern, relative)

    def _get_word(self, pattern: str) -> typing.Union[str, None]:
        """获取表格外的指定文字"""
        return PdfUtil.filter_word(self.words, pattern)
