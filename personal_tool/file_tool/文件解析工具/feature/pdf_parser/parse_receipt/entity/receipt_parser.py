import abc
import logging
import typing

from common_util.file_util.pdf_util.pdf_utils.entity.pdf_profile import TableProfile
from .receipt import Receipt
from ...base.pdf_parser_base import PdfParserBase


class ReceiptParser(PdfParserBase, metaclass=abc.ABCMeta):
    parser_name = "银行回单"

    def __init__(self, bank_name: str, receipt_path: str, **kwargs):
        super().__init__(bank_name, receipt_path, **kwargs)  # 银行名称
        self.receipts: typing.List[Receipt] = []

    def _parse_receipt(self, profile: TableProfile, type_class):
        """解析"""
        if not profile.table and not profile.words:
            return  # 跳过没有表格和文本的页
        _types = []
        for type_class in type_class.__subclasses__():
            _type = type_class(profile)
            # noinspection PyBroadException
            try:
                if _type.judge():
                    _types.append(_type)
            except Exception:
                pass
        if not len(_types):
            raise ValueError(f"{self.parser_type}回单pdf中有无法解析的回单")
        elif len(_types) > 1:
            logging.error(f"{self.parser_type}回单pdf中有匹配多个格式的回单: {[each.__str__() for each in _types]}")
            raise ValueError(f"{self.parser_type}回单pdf中有匹配多个格式的回单")
        else:
            receipt = _types[0].get_receipt()
            if receipt:
                self.receipts.append(receipt)
