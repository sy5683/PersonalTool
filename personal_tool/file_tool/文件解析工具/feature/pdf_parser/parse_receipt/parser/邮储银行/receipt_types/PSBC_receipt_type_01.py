import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .PSBC_receipt_type import PSBCReceiptType
from ....entity.receipt import Receipt


class PSBCReceiptType01(PSBCReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if {"付款方", "收款方", "户名"} < set(self.table.get_row_values(1)):
            return True
        if {"转出方", "转入方", "户名"} < set(self.table.get_row_values(1)):
            return True
        return False

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.type = self.__str__()  # 类型
        receipt.bank = self.bank_name  # 银行
        receipt.date = TimeUtil.format_to_str(self._get_cell_relative("^交易时间$").get_value())  # 日期
        receipt.receipt_number = self._get_cell_relative("^回单编号$").get_value()  # 回单编号
        receipt.serial_number = self._get_cell_relative("^交易流水号$").get_value()  # 流水号
        name_row_cells = self.table.get_row_cells(1)
        number_row_cells = self.table.get_row_cells(2)
        bank_row_cells = self.table.get_row_cells(3)
        if re.search("付款方|转出方", name_row_cells[0].get_value()):
            receipt.payer_account_name = name_row_cells[2].get_value()  # 付款人户名
            receipt.payer_account_number = number_row_cells[1].get_value()  # 付款人账号
            receipt.payer_account_bank = bank_row_cells[1].get_value()  # 付款人开户银行
            receipt.payee_account_name = name_row_cells[5].get_value()  # 收款人户名
            receipt.payee_account_number = number_row_cells[3].get_value()  # 收款人账号
            receipt.payee_account_bank = bank_row_cells[3].get_value()  # 收款人开户银行
        elif re.search("收款方|转入方", name_row_cells[0].get_value()):
            receipt.payer_account_name = name_row_cells[5].get_value()  # 付款人户名
            receipt.payer_account_number = number_row_cells[3].get_value()  # 付款人账号
            receipt.payer_account_bank = bank_row_cells[3].get_value()  # 付款人开户银行
            receipt.payee_account_name = name_row_cells[2].get_value()  # 收款人户名
            receipt.payee_account_number = number_row_cells[1].get_value()  # 收款人账号
            receipt.payee_account_bank = bank_row_cells[1].get_value()  # 收款人开户银行
        receipt.amount = NumberUtil.to_amount(
            self._get_cell_relative("^(收入|支出)金额[(（]小写[)）]$").get_value())  # 金额
        receipt.abstract = ""  # 摘要
        receipt.image = self.image  # 图片
        return receipt
