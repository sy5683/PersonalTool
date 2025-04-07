import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CIB_receipt_type import CIBReceiptType
from ....entity.receipt import Receipt


class CIBReceiptType04(CIBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if {"付款人", "收款人"} != set(self.table.get_row_values(0)):
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.type = self.__str__()  # 类型
        receipt.bank = self.bank_name  # 银行
        receipt.date = TimeUtil.format_to_str(self._get_word("^.*年.*月.*日$"))  # 日期
        direction_row_cells = self.table.get_row_cells(0)
        for row in range(1, 4):
            row_cells = self.table.get_row_cells(row)
            if re.search("收款人", direction_row_cells[0].get_value()):
                row_cells = row_cells[::-1]
            pattern = re.compile("全称[:：]")
            if pattern.search("".join([cell.get_value() for cell in row_cells])):
                receipt.payer_account_name = pattern.sub("", row_cells[0].get_value())  # 付款人户名
                receipt.payee_account_name = pattern.sub("", row_cells[1].get_value())  # 收款人户名
            pattern = re.compile("账号[:：]")
            if pattern.search("".join([cell.get_value() for cell in row_cells])):
                receipt.payer_account_number = pattern.sub("", row_cells[0].get_value())  # 付款人账号
                receipt.payee_account_number = pattern.sub("", row_cells[1].get_value())  # 收款人账号
            pattern = re.compile("开户银行[:：]")
            if pattern.search("".join([cell.get_value() for cell in row_cells])):
                receipt.payer_account_bank = pattern.sub("", row_cells[0].get_value())  # 付款人开户银行
                receipt.payee_account_bank = pattern.sub("", row_cells[1].get_value())  # 收款人开户银行
        pattern = "小写[:：](.*?)$"
        amount_cell = self.table.get_cell_relative(pattern, 0)
        receipt.amount = NumberUtil.to_amount(re.search(pattern, amount_cell.get_value()).group(1))  # 金额
        receipt.abstract = ""  # 摘要
        receipt.image = self.image  # 图片
        return receipt
