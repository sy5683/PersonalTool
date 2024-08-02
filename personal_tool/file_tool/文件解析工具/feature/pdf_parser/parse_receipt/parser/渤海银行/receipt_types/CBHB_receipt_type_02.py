from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CBHB_receipt_type import CBHBReceiptType
from ....entity.receipt import Receipt


class CBHBReceiptType02(CBHBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if "企业网上银行业务收费回单" not in self.table.get_cell(0, 0).get_value():
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_to_str(self.table.get_cell(1, 1).get_value())  # 日期
        receipt.payer_account_name = self.table.get_cell(2, 1).get_value()  # 付款人户名
        receipt.payer_account_number = self.table.get_cell(2, 3).get_value()  # 付款人账号
        receipt.amount = NumberUtil.to_amount(self.table.get_cell(5, 3).get_value())  # 金额
        return receipt
