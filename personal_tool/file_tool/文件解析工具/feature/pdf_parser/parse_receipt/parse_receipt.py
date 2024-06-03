from pathlib import Path

from common_util.code_util.import_util.import_util import ImportUtil
from .entity.receipt_parser import ReceiptParser
from ..base.pdf_parse_base import PdfParseBase


class ParseReceipt(PdfParseBase):
    ImportUtil.import_modules(Path(__file__).parent.joinpath("parser"))

    @classmethod
    def parse_receipt(cls, receipt_path: str, **kwargs) -> ReceiptParser:
        """解析银行回单"""
        return cls._parse(receipt_path, ReceiptParser, **kwargs)
