import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CDB_receipt_type import CDBReceiptType
from ....entity.receipt import Receipt


class CDBReceiptType03(CDBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if self.table.get_row_values(0)[0] != "国家开发银行网上银行电子回执":
            return False
        for key in ["付款人", "收款人", "全称"]:
            if key not in "".join(self.table.get_row_values(2)):
                return False
        return True

    def get_receipt(self) -> Receipt:
        """解析回单"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_time(re.findall("日期[:：](.*?)凭证号", self.table.get_row_values(1)[0])[0])  # 日期
        name_row_values = self.table.get_row_values(2)
        if name_row_values[0] == "付款人":
            receipt.payer_account_name = self._get_name(name_row_values[1])  # 付款人户名
            receipt.payer_account_number = self._get_account(self.table.get_row_values(3)[0])  # 付款人账号
            receipt.payee_account_name = self._get_name(name_row_values[3])  # 收款人户名
            receipt.payee_account_number = self._get_account(self.table.get_row_values(3)[1])  # 收款人账号
        elif name_row_values[0] == "收款人":
            receipt.payer_account_name = self._get_name(name_row_values[3])  # 付款人户名
            receipt.payer_account_number = self._get_account(self.table.get_row_values(3)[1])  # 付款人账号
            receipt.payee_account_name = self._get_name(name_row_values[1])  # 收款人户名
            receipt.payee_account_number = self._get_account(self.table.get_row_values(3)[0])  # 收款人账号
        receipt.amount = NumberUtil.to_amount(self.table.get_row_values(5)[3])  # 金额
        return receipt
