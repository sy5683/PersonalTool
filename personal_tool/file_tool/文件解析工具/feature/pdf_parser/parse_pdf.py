import typing
from pathlib import Path

from .parse_receipt.entity.receipt_parser import ReceiptParser
from .parse_receipt.parse_receipt import ParseReceipt
from .parse_voucher.entity.voucher_parser import VoucherParser
from .parse_voucher.parse_voucher import ParseVoucher


class ParsePdf:

    @staticmethod
    def parse_receipt(receipt_path: typing.Union[Path, str], **kwargs) -> ReceiptParser:
        """解析银行回单"""
        return ParseReceipt.parse_receipt(str(receipt_path), **kwargs)

    @staticmethod
    def parse_voucher(voucher_path: typing.Union[Path, str], **kwargs) -> VoucherParser:
        """解析电子凭证"""
        return ParseVoucher.parse_voucher(str(voucher_path), **kwargs)
