import typing
from pathlib import Path


class ParsePdf:

    @staticmethod
    def parse_receipt(receipt_path: typing.Union[Path, str], **kwargs):
        """解析银行回单"""
