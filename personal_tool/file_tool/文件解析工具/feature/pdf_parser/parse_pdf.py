import pathlib
import typing

from .parse_declaration.entity.declaration_parser import DeclarationParser
from .parse_declaration.parse_declaration import ParseDeclaration
from .parse_invoice.entity.invoice_parser import InvoiceParser
from .parse_invoice.parse_invoice import ParseInvoice
from .parse_receipt.entity.receipt_parser import ReceiptParser
from .parse_receipt.parse_receipt import ParseReceipt
from .parse_voucher.entity.voucher_parser import VoucherParser
from .parse_voucher.parse_voucher import ParseVoucher


class ParsePdf:

    @staticmethod
    def parse_declaration(declaration_path: typing.Union[pathlib.Path, str], **kwargs) -> DeclarationParser:
        """解析申报表"""
        return ParseDeclaration.parse_declaration(str(declaration_path), **kwargs)

    @staticmethod
    def parse_invoice(invoice_path: typing.Union[pathlib.Path, str], **kwargs) -> InvoiceParser:
        """解析银行回单"""
        return ParseInvoice.parse_invoice(str(invoice_path), **kwargs)

    @staticmethod
    def parse_receipt(receipt_path: typing.Union[pathlib.Path, str], **kwargs) -> ReceiptParser:
        """解析银行回单"""
        return ParseReceipt.parse_receipt(str(receipt_path), **kwargs)

    @staticmethod
    def parse_voucher(voucher_path: typing.Union[pathlib.Path, str], **kwargs) -> VoucherParser:
        """解析电子凭证"""
        return ParseVoucher.parse_voucher(str(voucher_path), **kwargs)
