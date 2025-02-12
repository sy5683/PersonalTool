import abc
import logging
import typing

from common_util.file_util.pdf_util.pdf_utils.entity.pdf_profile import TableProfile
from .invoice import Invoice
from ...base.pdf_parser_base import PdfParserBase


class InvoiceParser(PdfParserBase, metaclass=abc.ABCMeta):
    parser_name = "电子发票"

    def __init__(self, invoice_type: str, receipt_path: str, **kwargs):
        super().__init__(invoice_type, receipt_path, **kwargs)  # 发票类型
        self.invoices: typing.List[Invoice] = []

    def _parse_invoice(self, profile: TableProfile, type_class):
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
                else:
                    del _type
            except Exception:
                pass
        if not len(_types):
            raise ValueError(f"{self.parser_type}发票pdf中有无法解析的发票")
        elif len(_types) > 1:
            logging.error(f"{self.parser_type}发票pdf中有匹配多个格式的发票: {[each.__str__() for each in _types]}")
            raise ValueError(f"{self.parser_type}发票pdf中有匹配多个格式的发票")
        else:
            invoice = _types[0].get_invoice()
            if invoice:
                self.invoices.append(invoice)

