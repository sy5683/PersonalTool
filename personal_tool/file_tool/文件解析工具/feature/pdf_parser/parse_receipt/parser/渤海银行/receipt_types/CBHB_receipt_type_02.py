from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CBHB_receipt_type import CBHBReceiptType
from ....entity.receipt import Receipt


class CBHBReceiptType02(CBHBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if "企业网上银行业务收费回单" not in self.table.get_row_values(0)[0]:
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析回单"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_to_str(self.table.get_row_values(1)[1])  # 日期
        receipt.payer_account_name = self.table.get_row_values(2)[1]  # 付款人户名
        receipt.payer_account_number = self.table.get_row_values(2)[3]  # 付款人账号
        receipt.amount = NumberUtil.to_amount(self.table.get_row_values(5)[3])  # 金额
        return receipt
