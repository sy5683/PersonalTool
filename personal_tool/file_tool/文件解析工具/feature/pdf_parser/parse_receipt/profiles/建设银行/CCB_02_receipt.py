import re

import fitz

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from ...entity.receipt import Receipt
from ...entity.receipt_profile import ReceiptProfile


class CCB01Receipt(ReceiptProfile):

    def __init__(self, receipt_path: str, **kwargs):
        super().__init__("建设银行", receipt_path, **kwargs)

    def judge(self) -> bool:
        """判断是否为当前格式"""
        with fitz.open(self.receipt_path) as pdf:
            if "中国建设银行单位客户专用回单" not in pdf[0].get_text():
                return False
        return True

    def parse_receipt(self):
        """解析回单"""
        for pdf_profile in self.pdf_profiles:
            date_words = [each for each in pdf_profile.words if re.search("日流水号", each.text)]
            for index, table in enumerate(pdf_profile.tables):
                receipt = Receipt()
                receipt.date = TimeUtil.format_time(re.findall(r"人民币(.*?)流水号", date_words[index].text)[0])  # 日期
                name_row_values = table.get_row_values(0)
                if name_row_values[0] == "付款人":
                    receipt.payer_account_name = self.__get_name(name_row_values[2])  # 付款人户名
                    receipt.payer_account_number = table.get_row_values(1)[1]  # 付款人账号
                    receipt.payee_account_name = self.__get_name(name_row_values[5])  # 收款人户名
                    receipt.payee_account_number = table.get_row_values(1)[3]  # 收款人账号
                elif name_row_values[0] == "收款人":
                    receipt.payer_account_name = self.__get_name(name_row_values[5])  # 付款人户名
                    receipt.payer_account_number = table.get_row_values(1)[3]  # 付款人账号
                    receipt.payee_account_name = self.__get_name(name_row_values[2])  # 收款人户名
                    receipt.payee_account_number = table.get_row_values(1)[1]  # 收款人账号
                receipt.amount = NumberUtil.to_amount(re.findall(r"￥(.*)", table.get_row_values(3)[1]))  # 金额
                self.receipts.append(receipt)

    @staticmethod
    def __get_name(value: str) -> str:
        return re.sub("全称", "", value)
