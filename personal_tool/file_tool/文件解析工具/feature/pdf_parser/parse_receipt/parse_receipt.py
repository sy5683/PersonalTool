import logging
import os
from pathlib import Path

from common_util.code_util.import_util.import_util import ImportUtil
from .entity.receipt_parser import ReceiptParser


class ParseReceipt:
    ImportUtil.import_modules(Path(__file__).parent.joinpath("parser"))

    @staticmethod
    def parse_receipt(receipt_path: str, **kwargs) -> ReceiptParser:
        """解析银行回单"""
        logging.info(f"解析银行回单: {receipt_path}")
        receipt_name = os.path.basename(receipt_path)
        parsers = []
        for parser_class in ReceiptParser.__subclasses__():
            parser = parser_class(receipt_path=receipt_path, **kwargs)
            if parser.judge():
                parsers.append(parser)
        if not len(parsers):
            raise ValueError(f"银行回单【{receipt_name}】无法识别")
        elif len(parsers) > 1:
            raise ValueError(
                f"银行回单【{receipt_name}】匹配多种格式: %s" % "、".join([each.bank_name for each in parsers]))
        else:
            receipt_parser = parsers[0]
            logging.info(f"银行回单【{receipt_name}】的类型为: {receipt_parser.bank_name}回单")
            receipt_parser.parse_receipt()  # 调用解析回单方法
            return receipt_parser
