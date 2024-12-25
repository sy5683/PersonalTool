import re

from common_util.data_util.number_util.number_util import NumberUtil
from common_util.data_util.time_util.time_util import TimeUtil
from .FC_receipt_type import FCReceiptType
from ....entity.receipt import Receipt


class FCReceiptType02(FCReceiptType):

    def judge(self) -> bool:
        """判断是否为当前格式"""
        for key in ["类型", "起息日期", "终息日期", "天数", "平均余额", "利率", "利息"]:
            if not re.search(key, "".join(self.table.get_row_values(0))):
                return False
        return True

    def get_receipt(self) -> Receipt:
        """解析"""
        receipt = Receipt()
        receipt.bank = self.bank_name  # 银行
        receipt.date = TimeUtil.format_to_str(self._get_word("^.*年.*月.*日$"))  # 日期
        receipt.receipt_number = self._get_word("^交易编号[:：](.*?)$")  # 回单编号
        receipt.payee_account_name = self._get_word("^账户名称[:：](.*?)$")  # 收款人户名
        receipt.payee_account_number = self._get_word("^账号[:：](.*?)$")  # 收款人账号
        receipt.amount = NumberUtil.to_amount(self._get_cell_relative("^利息合计", 2).get_value())  # 金额
        receipt.image = self.image  # 图片
        return receipt
