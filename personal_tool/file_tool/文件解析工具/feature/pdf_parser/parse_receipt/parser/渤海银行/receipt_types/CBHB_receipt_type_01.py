import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CBHB_receipt_type import CBHBReceiptType
from ....entity.receipt import Receipt


class CBHBReceiptType01(CBHBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        for key in ["付款方", "收款方", "账号"]:
            if key not in "".join(self.table.get_row_values(1)):
                return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_to_str(self._get_cell_relative("^交易日期$").get_value())  # 日期
        receipt.serial_number = self._get_cell_relative(r"^网银流水号$").get_value()  # 流水号
        number_row_cells = self.table.get_row_cells(1)
        name_row_cells = self.table.get_row_cells(2)
        bank_row_cells = self.table.get_row_cells(3)
        if re.search("付款方", number_row_cells[0].get_value()):
            receipt.payer_account_name = name_row_cells[1].get_value()  # 付款人户名
            receipt.payer_account_number = number_row_cells[2].get_value()  # 付款人账号
            receipt.payer_account_bank = bank_row_cells[1].get_value()  # 付款人开户银行
            receipt.payee_account_name = name_row_cells[3].get_value()  # 收款人户名
            receipt.payee_account_number = number_row_cells[5].get_value()  # 收款人账号
            receipt.payee_account_bank = bank_row_cells[3].get_value()  # 收款人开户银行
        elif re.search("收款方", number_row_cells[0].get_value()):
            receipt.payer_account_name = name_row_cells[3].get_value()  # 付款人户名
            receipt.payer_account_number = number_row_cells[5].get_value()  # 付款人账号
            receipt.payer_account_bank = bank_row_cells[3].get_value()  # 付款人开户银行
            receipt.payee_account_name = name_row_cells[1].get_value()  # 收款人户名
            receipt.payee_account_number = number_row_cells[2].get_value()  # 收款人账号
            receipt.payee_account_bank = bank_row_cells[1].get_value()  # 收款人开户银行
        receipt.amount = NumberUtil.to_amount(self._get_cell_relative("^小写金额").get_value())  # 金额
        return receipt
