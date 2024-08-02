import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CCB_receipt_type import CCBReceiptType
from ....entity.receipt import Receipt


class CCBReceiptType01(CCBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if self.table.get_cell(0,0).get_value() != "中国建设银行网上银行电子回执":
            return False
        if len(self.table.get_row_values(2)) != 4:
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        date = re.findall("日期[:：](.*?)凭证号", self.table.get_cell(1, 0).get_value())[0]
        receipt.date = TimeUtil.format_to_str(date)  # 日期
        name_row_values = self.table.get_row_values(2)
        number_row_values = self.table.get_row_values(3)
        if name_row_values[0] == "付款人":
            receipt.payer_account_name = self._get_name(name_row_values[1])  # 付款人户名
            receipt.payer_account_number = self._get_account(number_row_values[0])  # 付款人账号
            receipt.payee_account_name = self._get_name(name_row_values[3])  # 收款人户名
            receipt.payee_account_number = self._get_account(number_row_values[1])  # 收款人账号
        elif name_row_values[0] == "收款人":
            receipt.payer_account_name = self._get_name(name_row_values[3])  # 付款人户名
            receipt.payer_account_number = self._get_account(number_row_values[1])  # 付款人账号
            receipt.payee_account_name = self._get_name(name_row_values[1])  # 收款人户名
            receipt.payee_account_number = self._get_account(number_row_values[0])  # 收款人账号
        receipt.amount = NumberUtil.to_amount(self.table.get_cell(5, 3).get_value())  # 金额
        return receipt
