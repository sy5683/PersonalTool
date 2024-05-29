import abc
import typing

from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .voucher import Voucher


class VoucherParser(metaclass=abc.ABCMeta):

    def __init__(self, voucher_type: str, voucher_path: str, **kwargs):
        self.voucher_type = voucher_type  # 凭证类型
        self.voucher_path = voucher_path  # 凭证路径
        self.pdf_profiles = PdfUtil.get_pdf_profiles(voucher_path)
        self.vouchers: typing.List[Voucher] = []

    @abc.abstractmethod
    def judge(self) -> bool:
        """判断是否为当前格式"""

    @abc.abstractmethod
    def parse_voucher(self):
        """解析凭证"""
