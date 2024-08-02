import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CBHB_receipt_type import CBHBReceiptType
from ....entity.receipt import Receipt


class CBHBReceiptType01(CBHBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        for key in ["付款方", "收款方", "账号"]:
            if key not in "".join(self.table.get_row_values(1)):
                return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_to_str(self.table.get_cell(7, 3).get_value())  # 日期
        account_row_values = self.table.get_row_values(1)
        name_row_values = self.table.get_row_values(2)
        if re.search("付款方", account_row_values[0]):
            receipt.payer_account_name = name_row_values[1]  # 付款人户名
            receipt.payer_account_number = account_row_values[2]  # 付款人账号
            receipt.payee_account_name = name_row_values[3]  # 收款人户名
            receipt.payee_account_number = account_row_values[5]  # 收款人账号
        elif re.search("收款方", account_row_values[0]):
            receipt.payer_account_name = name_row_values[3]  # 付款人户名
            receipt.payer_account_number = account_row_values[5]  # 付款人账号
            receipt.payee_account_name = name_row_values[1]  # 收款人户名
            receipt.payee_account_number = account_row_values[2]  # 收款人账号
        receipt.amount = NumberUtil.to_amount(self.table.get_cell(5, 1).get_value())  # 金额
        return receipt
