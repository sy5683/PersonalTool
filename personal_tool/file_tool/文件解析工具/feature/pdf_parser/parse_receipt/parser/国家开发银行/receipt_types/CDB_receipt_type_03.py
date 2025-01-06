import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CDB_receipt_type import CDBReceiptType
from ....entity.receipt import Receipt


class CDBReceiptType03(CDBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if self.table.get_row_values(0)[0] != "国家开发银行网上银行电子回执":
            return False
        for key in ["付款人", "收款人", "全称"]:
            if not re.search(key, "".join(self.table.get_row_values(2))):
                return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.type = self.__str__()  # 类型
        receipt.bank = self.bank_name  # 银行
        date = re.findall("日期[:：](.*?)凭证号", self.table.get_cell(1, 0).get_value())[0]
        receipt.date = TimeUtil.format_to_str(date)  # 日期
        receipt.serial_number = re.findall(r"交易流水号[:：](.*?)$", self.table.get_cell(1, 0).get_value())[0]  # 流水号
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
        receipt.amount = NumberUtil.to_amount(self._get_cell_relative("小写金额").get_value())  # 金额
        receipt.abstract = ""  # 摘要
        receipt.image = self.image  # 图片
        return receipt
