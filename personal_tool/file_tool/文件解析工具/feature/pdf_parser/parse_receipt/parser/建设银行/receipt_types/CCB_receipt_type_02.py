from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CCB_receipt_type import CCBReceiptType
from ....entity.receipt import Receipt


class CCBReceiptType02(CCBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if not {"付款人", "收款人", "全称"} < set(self.table.get_row_values(0)):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_to_str(self._get_word("人民币(.*?)流水号") or self._get_word(".*年.*月.*日"))  # 日期
        name_row_values = self.table.get_row_values(0)
        number_row_values = self.table.get_row_values(1)
        if name_row_values[0] == "付款人":
            receipt.payer_account_name = name_row_values[2]  # 付款人户名
            receipt.payer_account_number = number_row_values[1]  # 付款人账号
            receipt.payee_account_name = name_row_values[5]  # 收款人户名
            receipt.payee_account_number = number_row_values[3]  # 收款人账号
        elif name_row_values[0] == "收款人":
            receipt.payer_account_name = name_row_values[5]  # 付款人户名
            receipt.payer_account_number = number_row_values[3]  # 付款人账号
            receipt.payee_account_name = name_row_values[2]  # 收款人户名
            receipt.payee_account_number = number_row_values[1]  # 收款人账号
        receipt.amount = NumberUtil.to_amount(self.table.get_row_values(3))  # 金额
        return receipt
