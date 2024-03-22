from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CBHB_receipt_type import CBHBReceiptType
from ....entity.receipt import Receipt


class CBHBReceiptType04(CBHBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if "大额来账一般支付凭证" not in self.table.get_row_values(0)[0]:
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析回单"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_to_str(self.table.get_row_values(2)[1])  # 日期
        receipt.payer_account_name = self.table.get_row_values(5)[3]  # 付款人户名
        receipt.payer_account_number = self.table.get_row_values(5)[1]  # 付款人账号
        receipt.payee_account_name = self.table.get_row_values(8)[1]  # 收款人户名
        receipt.payee_account_number = self.table.get_row_values(7)[1]  # 收款人账号
        receipt.amount = NumberUtil.to_amount(self.table.get_row_values(9)[3])  # 金额
        return receipt
