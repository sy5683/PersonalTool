from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .ICBC_receipt_type import ICBCReceiptType
from ....entity.receipt import Receipt


class ICBCReceiptType01(ICBCReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if not {"付款人", "户名", "收款人"} < set(self.table.get_row_values(0)):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_to_str(self.table.get_cell(6,3).get_value())  # 日期
        receipt.payer_account_name = self.table.get_cell(0,2).get_value()  # 付款人户名
        receipt.payer_account_number = self._get_account(self.table.get_cell(1,1).get_value())  # 付款人账号
        receipt.payee_account_name = self.table.get_cell(0,5).get_value()  # 收款人户名
        receipt.payee_account_number = self._get_account(self.table.get_cell(1,3).get_value())  # 收款人账号
        receipt.amount = NumberUtil.to_amount(self.table.get_cell(3,1).get_value())  # 金额
        return receipt
