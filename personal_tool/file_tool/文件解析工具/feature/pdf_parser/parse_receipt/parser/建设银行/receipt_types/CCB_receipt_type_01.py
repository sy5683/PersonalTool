import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CCB_receipt_type import CCBReceiptType
from ....entity.receipt import Receipt


class CCBReceiptType01(CCBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if self.table.get_cell(0, 0).get_value() != "中国建设银行网上银行电子回执":
            return False
        if len(self.table.get_row_values(2)) not in [4, 6]:
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        # 建行这个格式的回单，日期、凭证号、流水号都在一个单元格中
        cell_value = self.table.get_cell(1, 0).get_value()
        receipt.date = TimeUtil.format_to_str(re.findall("日期[:：](.*?)凭证号", cell_value)[0])  # 日期
        receipt.receipt_number = re.findall(r"凭证号[:：](.*?)账户明细编号-交易流水号", cell_value)[0]  # 回单编号
        receipt.serial_number = re.findall("账户明细编号-交易流水号[:：](.*?)$", cell_value)[0]  # 流水号
        name_row_cells = self.table.get_row_cells(2)
        number_row_cells = self.table.get_row_cells(3)
        bank_row_cells = self.table.get_row_cells(4)
        if re.search("付款人", name_row_cells[0].get_value()):
            receipt.payer_account_name = self._get_name(name_row_cells[1].get_value())  # 付款人户名
            receipt.payer_account_number = self._get_account(number_row_cells[0].get_value())  # 付款人账号
            receipt.payer_account_bank = self._get_bank(bank_row_cells[0].get_value())  # 付款人开户银行
            receipt.payee_account_name = self._get_name(name_row_cells[3].get_value())  # 收款人户名
            receipt.payee_account_number = self._get_account(number_row_cells[1].get_value())  # 收款人账号
            receipt.payee_account_bank = self._get_bank(bank_row_cells[1].get_value())  # 收款人开户银行
        elif re.search("收款人", name_row_cells[0].get_value()):
            receipt.payer_account_name = self._get_name(name_row_cells[3].get_value())  # 付款人户名
            receipt.payer_account_number = self._get_account(number_row_cells[1].get_value())  # 付款人账号
            receipt.payer_account_bank = self._get_bank(bank_row_cells[1].get_value())  # 付款人开户银行
            receipt.payee_account_name = self._get_name(name_row_cells[1].get_value())  # 收款人户名
            receipt.payee_account_number = self._get_account(number_row_cells[0].get_value())  # 收款人账号
            receipt.payee_account_bank = self._get_bank(bank_row_cells[0].get_value())  # 收款人开户银行
        receipt.amount = NumberUtil.to_amount(self._get_cell_relative("^小写金额$").get_value())  # 金额
        return receipt
