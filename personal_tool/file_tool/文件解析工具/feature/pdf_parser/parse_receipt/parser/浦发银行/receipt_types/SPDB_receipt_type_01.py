import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .SPDB_receipt_type import SPDBReceiptType
from ....entity.receipt import Receipt


class SPDBReceiptType01(SPDBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if not {"付款人", "收款人", "账户名称"} < set(self.table.get_row_values(2)):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析回单"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_to_str(self.table.get_row_values(6)[1])  # 日期
        name_row_values = self.table.get_row_values(2)
        if re.search("付款人", name_row_values[0]):
            receipt.payer_account_name = name_row_values[2]  # 付款人户名
            receipt.payer_account_number = self.table.get_row_values(3)[1]  # 付款人账号
            receipt.payee_account_name = name_row_values[5]  # 收款人户名
            receipt.payee_account_number = self.table.get_row_values(3)[3]  # 收款人账号
        elif re.search("收款人", name_row_values[0]):
            receipt.payer_account_name = name_row_values[5]  # 付款人户名
            receipt.payer_account_number = self.table.get_row_values(3)[3]  # 付款人账号
            receipt.payee_account_name = name_row_values[2]  # 收款人户名
            receipt.payee_account_number = self.table.get_row_values(3)[1]  # 收款人账号
        receipt.amount = NumberUtil.to_amount(self.table.get_row_values(7)[3])  # 金额
        return receipt
