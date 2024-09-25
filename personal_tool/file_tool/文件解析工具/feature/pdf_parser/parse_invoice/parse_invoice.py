from pathlib import Path

from common_util.code_util.import_util.import_util import ImportUtil
from .entity.invoice_parser import InvoiceParser
from ..base.pdf_parse_base import PdfParseBase


class ParseInvoice(PdfParseBase):
    ImportUtil.import_modules(Path(__file__).parent.joinpath("parser"))

    @classmethod
    def parse_invoice(cls, invoice_path: str, **kwargs) -> InvoiceParser:
        """解析电子发票"""
        return cls._parse(invoice_path, InvoiceParser, **kwargs)
