from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .ICBC_receipt_type import ICBCReceiptType
from ....entity.receipt import Receipt


class CDBReceiptType01(ICBCReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if not {"付款人", "户名", "收款人", "户名"} < set(self.table.get_row_values(0)):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析回单"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_time(self.table.get_row_values(6)[3])  # 日期
        receipt.payer_account_name = self.table.get_row_values(0)[2]  # 付款人户名
        receipt.payer_account_number = self.table.get_row_values(1)[1]  # 付款人账号
        receipt.payee_account_name = self.table.get_row_values(0)[5]  # 收款人户名
        receipt.payee_account_number = self.table.get_row_values(1)[3]  # 收款人账号
        receipt.amount = NumberUtil.to_amount(self.table.get_row_values(3)[1])  # 金额
        return receipt
