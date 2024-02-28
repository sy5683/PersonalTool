import fitz

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from common_util.file_util.pdf_util.pdf_util import PdfUtil
from .receipt_types.CDB_receipt_type_01 import CDBReceiptType
from ...entity.receipt import Receipt
from ...entity.receipt_parser import ReceiptParser


class CDBReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("国开行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        with fitz.open(self.receipt_path) as pdf:
            if "国家开发银行" not in pdf[0].get_text():
                return False
        return True

    def parse_receipt(self):
        """解析回单"""
        for pdf_profile in self.pdf_profiles:
            for receipt_profile in PdfUtil.split_receipt_pdf(pdf_profile):
                receipt_types = []
                for receipt_type_class in CDBReceiptType.__subclasses__():
                    receipt_type = receipt_type_class(receipt_profile)
                    if receipt_type.judge():
                        receipt_types.append(receipt_type)
                if not len(receipt_types):
                    raise ValueError(f"{self.bank_name}回单pdf中有无法解析的回单")
                elif len(receipt_types) > 1:
                    raise ValueError(f"{self.bank_name}回单pdf中有匹配多个格式的回单")
                else:
                    self.receipts.append(receipt_types[0].get_receipt())
