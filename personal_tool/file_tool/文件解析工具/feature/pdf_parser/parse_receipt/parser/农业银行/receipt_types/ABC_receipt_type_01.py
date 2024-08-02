from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .ABC_receipt_type import ABCReceiptType
from ....entity.receipt import Receipt


class ABCReceiptType01(ABCReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if "账号" not in self.table.get_row_values(1):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_to_str(self.table.get_cell(7, 1).get_value())  # 日期
        number_row_values = self.table.get_row_values(1)
        name_row_values = self.table.get_row_values(2)
        bank_row_values = self.table.get_row_values(3)
        if number_row_values[0] == "付款方":
            receipt.payer_account_name = name_row_values[1]  # 付款人户名
            receipt.payer_account_number = number_row_values[2]  # 付款人账号
            receipt.payer_account_bank = bank_row_values[1]  # 付款人开户银行
            receipt.payee_account_name = name_row_values[3]  # 收款人户名
            receipt.payee_account_number = number_row_values[5]  # 收款人账号
            receipt.payee_account_bank = bank_row_values[3]  # 收款人开户银行
        elif number_row_values[0] == "收款方":
            receipt.payer_account_name = name_row_values[3]  # 付款人户名
            receipt.payer_account_number = number_row_values[5]  # 付款人账号
            receipt.payer_account_bank = bank_row_values[3]  # 付款人开户银行
            receipt.payee_account_name = name_row_values[1]  # 收款人户名
            receipt.payee_account_number = number_row_values[2]  # 收款人账号
            receipt.payee_account_bank = bank_row_values[1]  # 收款人开户银行
        receipt.amount = NumberUtil.to_amount(self.table.get_cell(4, 1).get_value())  # 金额
        return receipt
