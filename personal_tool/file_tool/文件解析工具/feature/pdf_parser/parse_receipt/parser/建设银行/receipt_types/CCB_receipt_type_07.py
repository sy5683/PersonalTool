import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CCB_receipt_type import CCBReceiptType
from ....entity.receipt import Receipt


class CCBReceiptType07(CCBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        for key in ["申请客户名称", "业务编号"]:
            if key not in "".join(self.table.get_row_values(0)):
                return False
        if not {"付款账号", "收款账号"} < set(self.table.get_row_values(1)):
            return False
        if len(self.table.get_row_values(5)) != 4:
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析回单"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_time(self._get_word(".*年.*月.*日"))  # 日期
        account_row_values = self.table.get_row_values(1)
        if account_row_values[0] == "付款账号":
            receipt.payer_account_name = self._get_name(self.table.get_row_values(2)[1])  # 付款人户名
            receipt.payer_account_number = account_row_values[1]  # 付款人账号
            receipt.payee_account_name = self._get_name(self.table.get_row_values(2)[3])  # 收款人户名
            receipt.payee_account_number = account_row_values[3]  # 收款人账号
        elif account_row_values[0] == "收款账号":
            receipt.payer_account_name = self._get_name(self.table.get_row_values(2)[3])  # 付款人户名
            receipt.payer_account_number = account_row_values[3]  # 付款人账号
            receipt.payee_account_name = self._get_name(self.table.get_row_values(2)[1])  # 收款人户名
            receipt.payee_account_number = account_row_values[1]  # 收款人账号
        receipt.amount = NumberUtil.to_amount(self.table.get_row_values(5)[3])  # 金额
        return receipt
