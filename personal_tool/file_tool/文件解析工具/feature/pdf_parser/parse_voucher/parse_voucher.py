import logging
import os
from pathlib import Path

from common_util.code_util.import_util.import_util import ImportUtil
from .entity.voucher_parser import VoucherParser


class ParseVoucher:
    ImportUtil.import_modules(Path(__file__).parent.joinpath("parser"))

    @staticmethod
    def parse_voucher(voucher_path: str, **kwargs) -> VoucherParser:
        """解析电子凭证"""
        logging.info(f"解析电子凭证: {voucher_path}")
        voucher_name = os.path.basename(voucher_path)
        parsers = []
        for parser_class in VoucherParser.__subclasses__():
            parser = parser_class(voucher_path=voucher_path, **kwargs)
            if parser.judge():
                parsers.append(parser)
        if not len(parsers):
            raise ValueError(f"电子凭证【{voucher_name}】无法识别")
        elif len(parsers) > 1:
            parsers_types = "、".join([parser.voucher_type for parser in parsers])
            raise ValueError(f"电子凭证【{voucher_name}】匹配多种格式: {parsers_types}")
        else:
            voucher_parser = parsers[0]
            logging.info(f"电子凭证【{voucher_name}】的类型为: {voucher_parser.voucher_type}回单")
            voucher_parser.parse_voucher()  # 调用解析凭证方法
            return voucher_parser
