import re

from .CCB_receipt_type import CCBReceiptType
from ....entity.receipt import Receipt


class CCBReceiptType05(CCBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        for key in ["项目名称", "工本费/转账汇款手续费/手续费", "金额"]:
            if key not in "".join(self.table.get_row_values(1)):
                return False
        if "合计金额" not in self.table.get_col_values(0):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析回单"""
        receipt = Receipt()
        receipt.date = self._get_date(".*年.*月.*日")  # 日期
        receipt.payer_account_name = re.sub("户名[:：]", "", self.table.get_row_values(0)[0])  # 付款人户名
        receipt.payer_account_number = re.sub("账号[:：]", "", self.table.get_row_values(0)[1])  # 付款人账号
        receipt.amount = self._get_amount(0, 2)  # 金额
        return receipt
