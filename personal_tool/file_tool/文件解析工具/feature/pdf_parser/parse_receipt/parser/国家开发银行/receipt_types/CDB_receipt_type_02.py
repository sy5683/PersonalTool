import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .CDB_receipt_type import CDBReceiptType
from ....entity.receipt import Receipt


class CDBReceiptType02(CDBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        for key in ["计息项目", "起息日", "结息日", "本金/积数", "利率", "利息"]:
            if not re.search(key, "".join(self.table.get_row_values(1))):
                return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_to_str(self._get_word("^.*年.*月.*日$"))  # 日期
        receipt.receipt_number = self._get_word(r"^[a-zA-Z\d+]+$")  # 回单编号
        receipt.serial_number = self._get_word("^流水号[:：](.*?)$")  # 流水号
        payee_account_row_cells = self.table.get_row_cells(0)
        receipt.payee_account_name = self._get_account(payee_account_row_cells[0].get_value())  # 收款人户名
        receipt.payee_account_number = self._get_account(payee_account_row_cells[1].get_value())  # 收款人账号
        receipt.amount = NumberUtil.to_amount(self._get_cell_relative("^合计金额").get_value())  # 金额
        return receipt
