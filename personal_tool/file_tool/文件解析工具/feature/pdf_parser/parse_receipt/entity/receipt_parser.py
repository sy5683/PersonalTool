import abc
import collections
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

    def _format_parser(self):
        """解析完成后对整张解析后的银行回单做收支类型等信息的提前和整合"""
        # 存储所有的回单付款方/收款方户名和账号
        receipt_numbers, receipt_names = [], []
        for receipt in self.receipts:
            receipt_names.append(receipt.payer_account_name)
            receipt_numbers.append(receipt.payer_account_number)
            receipt_names.append(receipt.payee_account_name)
            receipt_numbers.append(receipt.payee_account_number)
        # 根据出现次数最多的户名和账号判断其回单的户名和账号
        receipt_names, receipt_numbers = collections.Counter(receipt_names), collections.Counter(receipt_numbers)
        receipt_name = max(receipt_names, key=receipt_names.get)
        receipt_number = max(receipt_numbers, key=receipt_numbers.get)
        # 判断每个账号收支类型
        for receipt in self.receipts:
            receipt.receipt_account_name = receipt_name
            receipt.receipt_account_number = receipt_number
            if receipt.payer_account_number == receipt_number:
                receipt.pay_type = "payment"
            elif receipt.payee_account_number == receipt_number:
                receipt.pay_type = "collection"
            else:
                receipt.pay_type = "error"
