import typing
from pathlib import Path

from .parse_receipt.parse_receipt import ParseReceipt


class ParsePdf:

    @staticmethod
    def parse_receipt(receipt_path: typing.Union[Path, str], **kwargs):
        """解析银行回单"""
        return ParseReceipt.parse_receipt(str(receipt_path), **kwargs)
