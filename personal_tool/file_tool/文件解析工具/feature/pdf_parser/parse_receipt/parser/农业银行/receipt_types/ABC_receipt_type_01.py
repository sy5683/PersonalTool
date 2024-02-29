from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .ABC_receipt_type import ABCReceiptType
from ....entity.receipt import Receipt


class ABCReceiptType01(ABCReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        print(self.table.get_row_values(1))
        if not {"付款方", "账号", "收款方", "账号"} < set(self.table.get_row_values(1)):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析回单"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_time(self.table.get_row_values(7)[1])  # 日期
        name_row_values = self.table.get_row_values(1)
        if name_row_values[0] == "付款方":
            receipt.payer_account_name = self.table.get_row_values(2)[1]  # 付款人户名
            receipt.payer_account_number = name_row_values[2]  # 付款人账号
            receipt.payee_account_name = self.table.get_row_values(2)[3]  # 收款人户名
            receipt.payee_account_number = name_row_values[5]  # 收款人账号
        elif name_row_values[0] == "收款方":
            receipt.payer_account_name = self.table.get_row_values(2)[3]  # 付款人户名
            receipt.payer_account_number = name_row_values[5]  # 付款人账号
            receipt.payee_account_name = self.table.get_row_values(2)[1]  # 收款人户名
            receipt.payee_account_number = name_row_values[2]  # 收款人账号
        receipt.amount = NumberUtil.to_amount(self.table.get_row_values(4)[1])  # 金额
        return receipt
