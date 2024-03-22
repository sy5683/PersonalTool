import re

from common_util.data_util.time_util.time_util import TimeUtil
from .CCB_receipt_type import CCBReceiptType
from ....entity.receipt import Receipt


class CCBReceiptType04(CCBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        for key in ["计息项目", "起息日", "结息日", "本金/积数", "利率", "利息"]:
            if key not in "".join(self.table.get_row_values(1)):
                return False
        if "合计金额" not in self.table.get_col_values(0):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析回单"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_to_str(self._get_word(".*年.*月.*日"))  # 日期
        receipt.payee_account_name = self._get_account(self.table.get_row_values(0)[0])  # 收款人户名
        receipt.payee_account_number = self._get_account(self.table.get_row_values(0)[1])  # 收款人账号
        receipt.amount = self._get_amount(0, 2)  # 金额
        return receipt
