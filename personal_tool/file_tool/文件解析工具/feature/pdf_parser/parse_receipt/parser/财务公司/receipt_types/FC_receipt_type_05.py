import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .FC_receipt_type import FCReceiptType
from ....entity.receipt import Receipt


class FCReceiptType05(FCReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        for key in ["类型", "本金", "手续费率", "手续费"]:
            if not re.search(key, "".join(self.table.get_row_values(0))):
                return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.date = TimeUtil.format_to_str(self._get_word("^.*年.*月.*日$"))  # 日期
        receipt.receipt_number = self._get_word("^交易编号[:：](.*?)$")  # 回单编号
        receipt.payer_account_name = self._get_word("^借款单位名称[:：](.*?)$")  # 付款人户名
        receipt.payer_account_number = self._get_word("^账号[:：](.*?)$")  # 付款人账号
        receipt.payee_account_name = self._get_word("^委托单位名称[:：](.*?)$")  # 收款人户名
        receipt.amount = NumberUtil.to_amount(self.table.get_cell(1, 3).get_value())  # 金额
        return receipt
