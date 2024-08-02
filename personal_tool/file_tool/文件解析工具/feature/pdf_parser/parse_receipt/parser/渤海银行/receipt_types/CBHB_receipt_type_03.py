from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CBHB_receipt_type import CBHBReceiptType
from ....entity.receipt import Receipt


class CBHBReceiptType03(CBHBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if "小额来账贷记凭证" not in self.table.get_cell(0, 0).get_value():
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_to_str(self.table.get_cell(2, 1).get_value())  # 日期
        receipt.payer_account_name = self.table.get_cell(6, 3).get_value()  # 付款人户名
        receipt.payer_account_number = self.table.get_cell(6, 1).get_value()  # 付款人账号
        receipt.payee_account_name = self.table.get_cell(8, 3).get_value()  # 收款人户名
        receipt.payee_account_number = self.table.get_cell(8, 1).get_value()  # 收款人账号
        receipt.amount = NumberUtil.to_amount(self.table.get_cell(10, 3).get_value())  # 金额
        return receipt
