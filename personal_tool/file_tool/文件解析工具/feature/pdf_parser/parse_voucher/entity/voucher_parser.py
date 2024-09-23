import abc
import typing

from .voucher import Voucher
from ...base.pdf_parser_base import PdfParserBase


class VoucherParser(PdfParserBase, metaclass=abc.ABCMeta):
    parser_name = "电子凭证"

    def __init__(self, voucher_type: str, voucher_path: str, **kwargs):
        super().__init__(voucher_type, voucher_path, **kwargs)  # 凭证类型
        self.vouchers: typing.List[Voucher] = []
