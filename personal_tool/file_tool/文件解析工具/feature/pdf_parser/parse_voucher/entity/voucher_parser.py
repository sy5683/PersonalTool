import abc
import typing

from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .voucher import Voucher
from ...base.pdf_parser_base import PdfParserBase


class VoucherParser(PdfParserBase, metaclass=abc.ABCMeta):
    parser_name = "电子凭证"

    def __init__(self, voucher_type: str, voucher_path: str, **kwargs):
        self.parser_type = voucher_type  # 凭证类型
        self.voucher_path = voucher_path  # 凭证路径
        self.pdf_profiles = PdfUtil.get_pdf_profiles(voucher_path)
        self.vouchers: typing.List[Voucher] = []
