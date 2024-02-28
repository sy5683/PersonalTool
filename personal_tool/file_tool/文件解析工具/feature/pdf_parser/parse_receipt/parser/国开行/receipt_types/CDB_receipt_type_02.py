import re

from common_util.data_util.number_util.number_util import NumberUtil
from .CDB_receipt_type import CDBReceiptType
from ....entity.receipt import Receipt


class CDBReceiptType02(CDBReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        if self.table.max_cols != 7:
            return False
        if self.table.get_row_values(1) != ["计息项目", "起息日", "结息日", "本金/积数", "利率(%)", "利息"]:
            return False
        return True

    def get_receipt(self) -> Receipt:
        """解析回单"""
        receipt = Receipt()
        receipt.date = self._get_date(".*年.*月.*日")  # 日期
        receipt.payee_account_name = re.sub("户名|:|：", "", self.table.get_row_values(0)[0])  # 收款人户名
        receipt.payee_account_number = re.sub("账号|:|：", "", self.table.get_row_values(0)[1])  # 收款人账号
        receipt.amount = self.__get_amount()  # 金额
        return receipt

    def __get_amount(self) -> float:
        """获取金额"""
        for row in range(self.table.max_rows):
            row_values = self.table.get_row_values(row)
            if row_values[0] == "合计金额":
                return NumberUtil.to_amount(row_values[2])
        raise ValueError("格式异常，回单无法提取金额")
