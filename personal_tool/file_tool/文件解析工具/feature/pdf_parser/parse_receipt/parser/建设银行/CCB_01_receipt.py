import re

import fitz

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from ...entity.receipt import Receipt
from ...entity.receipt_parser import ReceiptParser


class CCB01ReceiptParser(ReceiptParser):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("建设银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        with fitz.open(self.receipt_path) as pdf:
            if "中国建设银行网上银行电子回执" not in pdf[0].get_text():
                return False
        return True

    def parse_receipt(self):
        """解析回单"""
        for pdf_profile in self.pdf_profiles:
            for table in pdf_profile.tables:
                receipt = Receipt()
                receipt.date = TimeUtil.format_time(re.findall("日期：(.*?)凭证号", table.get_row_values(1)[0])[0])  # 日期
                name_row_values = table.get_row_values(2)
                if name_row_values[0] == "付款人":
                    receipt.payer_account_name = self.__get_name(name_row_values[1])  # 付款人户名
                    receipt.payer_account_number = self.__get_account(table.get_row_values(3)[0])  # 付款人账号
                    receipt.payee_account_name = self.__get_name(name_row_values[3])  # 收款人户名
                    receipt.payee_account_number = self.__get_account(table.get_row_values(3)[1])  # 收款人账号
                elif name_row_values[0] == "收款人":
                    receipt.payer_account_name = self.__get_name(name_row_values[3])  # 付款人户名
                    receipt.payer_account_number = self.__get_account(table.get_row_values(3)[1])  # 付款人账号
                    receipt.payee_account_name = self.__get_name(name_row_values[1])  # 收款人户名
                    receipt.payee_account_number = self.__get_account(table.get_row_values(3)[0])  # 收款人账号
                receipt.amount = NumberUtil.to_amount(table.get_row_values(5)[3])  # 金额
                self.receipts.append(receipt)

    @staticmethod
    def __get_account(value: str) -> str:
        return re.sub("账号", "", value)

    @staticmethod
    def __get_name(value: str) -> str:
        return re.sub("全称", "", value)
