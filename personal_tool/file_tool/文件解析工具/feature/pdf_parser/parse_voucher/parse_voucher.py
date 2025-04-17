from pathlib import pathlib.Path

from common_util.code_util.import_util.import_util import ImportUtil
from .entity.voucher_parser import VoucherParser
from ..base.pdf_parse_base import PdfParseBase


class ParseVoucher(PdfParseBase):
    ImportUtil.import_modules(pathlib.Path(__file__).parent.joinpath("parser"))

    @classmethod
    def parse_voucher(cls, voucher_path: str, **kwargs) -> VoucherParser:
        """解析电子凭证"""
        return cls._parse(voucher_path, VoucherParser, **kwargs)
